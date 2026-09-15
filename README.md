# Radio.de for Kodi Piers

Independent maintenance source for `IkHadHonger/plugin.audio.radio.de`.
Based on the user-supplied `plugin.audio.radiode-1.1.13-kodi22(1).zip`, not a
verified export of an upstream Git commit. Original author: fivebanger.
The included GPL version 2 license and existing author attribution are retained.
This project is not endorsed by Radio.de. Upstream activity has not been verified.

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
CI builds and checks pull requests and pushes to `main`; it never publishes them.

## Initial GitHub setup

1. Source is maintained in `IkHadHonger/plugin.audio.radio.de` on `main`.
   The Kodi addon ID is `plugin.audio.radiode`; it differs from the repository name.
2. Check that the Build workflow passes. Install its ZIP on the Cube and test
   station search, favourites, playback, station switching and podcasts.
3. To enable publication, configure `REPO_SILVO_PAT` in this source repository's
   Actions secrets. It needs Contents read/write on `IkHadHonger/repository.silvo`.
   A secret configured in another repository is not automatically shared here.
4. Run Publish Piers manually on `main` after testing. This writes only the radio
   package and Piers indexes in `repository.silvo`, branch `cube-custom`.

There is no upstream synchronization or automatic deployment on push. AVDVPlus
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
