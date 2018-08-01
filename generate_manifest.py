import json

import click

from ethpm import ASSETS_DIR
from ethpm.constants import PACKAGE_NAME_REGEX
from ethpm.exceptions import ValidationError
from ethpm.manifest import Manifest
from ethpm.validation import validate_package_name

MANIFESTS_DIR = ASSETS_DIR / "manifests"


@click.command()
def main():
    """
    CLI tool to guide user through manifest generation process.
    """
    click.echo("")
    click.echo("🌸            Welcome to Py-EthPM            🌸")
    click.echo("This program comes with ABSOLUTELY NO WARRANTY.")
    click.echo("")
    click.echo("To create your own manifest, please provide the following data.")
    # Generate required manifest data
    manifest_version = get_manifest_version()
    package_name = get_package_name()
    version = get_version()
    manifest = Manifest(manifest_version, package_name, version)
    # Generate optional metadata
    click.echo("")
    click.echo("The meta field defines a location for metadata about the package which")
    click.echo("is not integral in nature for package installation, but may be")
    click.echo("important or convenient to have on-hand for other reasons.")
    click.echo("*  Packages should include this field  *")
    click.echo("")
    include_meta = boolean("Do you want to include meta?")
    if include_meta:
        manifest.meta = get_metadata()
    # Generate optional contract sources
    click.echo("")
    click.echo("The sources field defines a source tree that should comprise the full")
    click.echo(
        "source tree necessary to recompile the contracts contained in this release."
    )
    click.echo("-  Sources are declared in a key/value mapping.")
    click.echo("-  Keys must be relative filesystem paths beginning with `./`")
    click.echo("-  Values must be a source string or content addressable URI")
    click.echo("")
    include_sources = boolean("Do you want to include source(s)?")
    if include_sources:
        manifest.sources = get_sources()
    # Manifest preview
    click.echo("")
    click.echo("🔥              Manifest Preview             🔥")
    click.echo(manifest.pretty())
    approve = boolean("Would you like to save this manifest to disk?")
    if approve:
        write_manifest_to_disk(manifest)
    click.echo("🌸         Thanks for using Py-EthPM         🌸")


def get_version():
    click.echo("")
    click.echo("The `version` field declares the version number of this release.")
    click.echo(
        "This value should conform to the semver version numbering specification."
    )
    click.echo("*  Packages must include this field  *")
    version = click.prompt("Please enter the package version")
    return version


def write_manifest_to_disk(manifest):
    minified_json = manifest.minified()
    package_manifest_dir = MANIFESTS_DIR / manifest.package_name
    package_manifest_dir.mkdir(exist_ok=True)
    manifest_path = package_manifest_dir / str(manifest.version + ".json")
    manifest_path.write_text(minified_json)
    click.echo("Compact manifest written to {0}".format(manifest_path))
    save_pretty = boolean(
        "Would you like to also save a human readable version of your manifest?"
    )
    if save_pretty:
        pretty_json = manifest.pretty()
        pretty_manifest_path = package_manifest_dir / str(
            manifest.version + "-pretty.json"
        )
        pretty_manifest_path.write_text(pretty_json)
        click.echo("Pretty manifest written to {0}".format(pretty_manifest_path))


def get_sources():
    number_of_sources = click.prompt("How many sources do you have?", type=int)
    sources = {}
    for num in range(number_of_sources):
        source_key = click.prompt(
            "Source [{0}/{1}] Key".format(num + 1, number_of_sources)
        )
        source_value = click.prompt(
            "Source [{0}/{1}] Value".format(num + 1, number_of_sources)
        )
        sources[source_key] = source_value
    return sources


def get_manifest_version():
    click.echo("")
    click.echo(
        "The `manifest_version` field defines the specification version that this document conforms to."
    )
    click.echo("*  Packages must include this field  *")
    manifest_version = click.prompt("Please enter your manifest version", type=int)
    if manifest_version is not 2:
        click.echo("Only Manifest V2 is supported.")
        return manifest_version()
    return manifest_version


def get_package_name():
    click.echo("")
    click.echo(
        "The `package_name` field defines a human readable name for this package."
    )
    click.echo(
        "Package names must conform to the regular expression: {0}".format(
            PACKAGE_NAME_REGEX
        )
    )
    click.echo("*  Packages must include this field  *")
    package_name = click.prompt("Please enter your package name")
    try:
        validate_package_name(package_name)
    except ValidationError:
        click.echo(
            "{0} is not a valid package name. Package names must conform to the regular expression: {1}".format(
                package_name, PACKAGE_NAME_REGEX
            )
        )
        return get_package_name()
    return package_name


def get_metadata():
    meta_dict = {}

    click.echo("")
    click.echo(
        "The `license` field declares the license under which this package is released."
    )
    click.echo("This value should conform to the SPDX format.")
    if boolean("Do you want to include a license in your metadata?"):
        license = click.prompt("License")
        meta_dict["license"] = license

    click.echo("")
    click.echo(
        "The `authors` field defines a list of human readable names for the authors of this package."
    )
    click.echo('Suggested format: "Author Name <author@email>"')
    if boolean("Do you want to include authors in your metadata?"):
        number_of_authors = click.prompt("How many authors?", type=int)
        authors = [
            click.prompt("Author [{0}/{1}]".format(num + 1, number_of_authors))
            for num in range(number_of_authors)
        ]
        meta_dict["authors"] = authors

    click.echo("")
    click.echo(
        "The `description` field provides additional detail that may be relevant for the package."
    )
    if boolean("Do you want to include a description in your metadata?"):
        description = click.prompt("Description")
        meta_dict["description"] = description

    click.echo("")
    click.echo(
        "The `keywords` field provides relevant keywords related to this package."
    )
    if boolean("Do you want to include any keywords in your metadata?"):
        number_of_keywords = click.prompt("How many keywords?", type=int)
        keywords = [
            click.prompt("Keyword [{0}/{1}]".format(num + 1, number_of_keywords))
            for num in range(number_of_keywords)
        ]
        meta_dict["keywords"] = keywords

    click.echo("")
    click.echo(
        "The `links` field provides URIs to relevant resources associated with this package."
    )
    click.echo(
        "When possible, authors should use the following keys for the following common resources."
    )
    click.echo("-  website: Primary website for the package")
    click.echo("-  documentation: Package Documentation")
    click.echo("-  repository: Location of the project source code")
    if boolean("Do you want to include any links in your metadata?"):
        number_of_links = click.prompt("How many links?", type=int)
        links = {}
        for num in range(number_of_links):
            link_key = click.prompt(
                "Link Key [{0}/{1}]".format(num + 1, number_of_links)
            )
            link_value = click.prompt(
                "Link Value [{0}/{1}]".format(num + 1, number_of_links)
            )
            links[link_key] = link_value
        meta_dict["links"] = links

    return meta_dict


def boolean(message):
    response = click.prompt(message + " [y/n]")
    if response == "y":
        return True
    if response == "n":
        return False
    click.echo("Invalid answer: [y/n]")
    return boolean(message)


if __name__ == "__main__":
    main()
