import subprocess  # nosec
from collections import defaultdict
from os.path import exists, isdir, isfile, join, normpath
from resolver import AResolver
from link import Link
from envelope import Envelope
from securesystemslib.signer import Signature, SSlibSigner


def record_artifacts_as_dict(
    artifacts,
    exclude_patterns=None,
    base_path=None,
    follow_symlink_dirs=False,
    normalize_line_endings=False,
    lstrip_paths=None,
):
    hashes = {}
    if not artifacts:
        return hashes
    if not base_path:
        base_path = None
    if not exclude_patterns:
        exclude_patterns = ["*.link*", ".git", "*.pyc", "*~"]

    # def _hash_artifacts(uris):
    #     for path in uris:
    #         path = normpath(path)
    #         if

    resolver = AResolver(
        exclude_patterns=None,
        base_path=base_path,
        follow_symlink_dirs=follow_symlink_dirs,
        normalize_line_endings=normalize_line_endings,
        lstrip_paths=lstrip_paths,
    )

    return resolver.hash_artifacts(artifacts)


# TODO: figure out record_streams
def execute_link(link_cmd_args, record_streams, timeout):
    process = subprocess.run(
        link_cmd_args,
        check=False,
        timeout=timeout,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    stdout_str = stderr_str = ""

    return {
        "stdout": stdout_str,
        "stderr": stderr_str,
        "returncode": process.returncode,
    }


FILENAME_FORMAT = "{step_name}.{keyid:.8}.link"


def run(
    name=None,
    product_list=None,
    link_cmd_args=None,
    record_streams=None,
    timeout=None,
    base_path=None,
    signing_key={},
):
    print("run...")
    # Run the subcommand
    # output = {'stdout': '', 'stderr': '', 'returncode': 0}
    byproducts = execute_link(link_cmd_args, record_streams, timeout)
    # Validate the products that were touched during the
    # execution of the subcommand
    products_dict = record_artifacts_as_dict(
        artifacts=product_list, base_path=base_path
    )

    # Generate a link:
    # metadata information gathered while performing a supply chain step or inspection,
    # signed by the functionary that performed the step or the client that performed
    # the inspection. This metadata includes information such as materials, products
    # and byproducts.
    environment = {}
    link = Link(
        name=name,
        products=products_dict,
        command=link_cmd_args,
        byproducts=byproducts,
        environment=environment,
    )

    # Create a method for signing the data
    envelope = Envelope.from_signable(link)
    print(envelope)

    signer = None

    # Create the actual entity that will be used to sign the data
    signer = SSlibSigner(signing_key)
    # TODO: Thought: what happens if we don't have a signer?
    if signer:
        # Add signature to the data
        signature = envelope.create_signature(signer)
        signing_keyid = signature.keyid

        # Export that data to disk
        filename = FILENAME_FORMAT.format(step_name=name, keyid=signing_keyid)
        envelope.dump(filename)

    return envelope
