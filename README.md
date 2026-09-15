# Radio.de for Kodi Piers

Independent maintenance source for `IkHadHonger/plugin.audio.radio.de`.
Based on the user-supplied `plugin.audio.radiode-1.1.13-kodi22(1).zip`, not a
verified export of an upstream Git commit. Original author: fivebanger.
The included GPL version 2 license and existing author attribution are retained.
This project is not endorsed by Radio.de.

Original upstream repository: [fivebanger/kodi_addons](https://github.com/fivebanger/kodi_addons).
The upstream [Radio.de directory](https://github.com/fivebanger/kodi_addons/tree/master/plugin.audio.radiode)
provides the original author's packaged addon. This repository independently
maintains the supplied Kodi 22 adaptation; it is not a GitHub fork of upstream.

## Scope

Target: CoreELEC 22 / Kodi Piers on Cube 3. The Python playback implementation
is unchanged from the supplied archive. Version 1.1.14 adds maintenance packaging
and metadata, and escapes an invalid ampersand in settings.xml without changing
the decoded action URL. Kodi runtime compatibility and live playback still need testing.
The addon ID stays `plugin.audio.radiode`, preserving the identity used by existing
settings and favourites. Select this repository as the update origin in Kodi if
another repository also supplies this ID.

## Build

Run `python tools/build.py` with Python 3.11 or newer. No build dependencies are
required. The output is `dist/plugin.audio.radiode-1.1.14.zip`.
CI builds and checks pull requests and pushes to `main`. After a successful push
build on `main`, Publish Piers automatically publishes a newer addon version.
Pull request builds never trigger publication. The exact successful source commit
is used. Documentation-only changes with the same version skip publication.

## Initial GitHub setup

1. Source is maintained in `IkHadHonger/plugin.audio.radio.de` on `main`.
   The Kodi addon ID is `plugin.audio.radiode`; it differs from the repository name.
2. Check that the Build workflow passes. Install its ZIP on the Cube and test
   station search, favourites, playback, station switching and podcasts.
3. To enable publication, configure `REPO_SILVO_PAT` in this source repository's
   Actions secrets. It needs Contents read/write on `IkHadHonger/repository.silvo`.
   A secret configured in another repository is not automatically shared here.
4. Test changes before merging to `main`, and increase the version in `addon.xml`
   for each addon release (for example, 1.1.14 to 1.1.15). The version is not
   automatically incremented. After a successful main push build, Publish Piers
   writes the newer package and Piers indexes to `repository.silvo`, branch
   `cube-custom`. Manual dispatch remains available for retries.

There is no upstream synchronization. Automatic publication targets Piers only. AVDVPlus
is not a publication target. Existing repository addon 1.0.3 needs no version bump
solely for adding an addon to its Piers catalogue.

## Releases and recovery

Increase `addon.xml` version and document each release. Publication refuses to
replace a different ZIP under an existing version or to downgrade a published
version. Old ZIPs remain available. If another publisher updates the target branch
during publication, the non-forced push fails; rerun against the latest branch.
To recover from a bad release, restore the working source and publish it with a
higher version. Never force-push the distribution branch.

## Checks and limitations

Build checks parse all Python/XML files, validate package identity and required
assets, and check ZIP integrity. These checks do not exercise Kodi, the Radio.de
API, receiver output, or station streams.

Known review items inherited from the supplied ZIP: the URL resolver treats M3U8
like a simple playlist and can follow a media segment instead of preserving HLS;
playlist bodies are read without a size limit; `_filter_result` assumes a mapping
although API errors return a list. These are recorded for targeted follow-up,
not silently changed during the repository import.
