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
build on `main`, Publish Piers compares the built addon ZIP with the published ZIP.
If the package changed at the same version, it increments the final version number
in `addon.xml` (for example, 1.1.14 to 1.1.15), validates the new package, and commits
that version to `main` before publication. An explicitly higher version is retained.
Pull requests and superseded main builds never publish. README-only changes do not
alter the package and therefore do not create a release.

## Initial GitHub setup

1. Source is maintained in `IkHadHonger/plugin.audio.radio.de` on `main`.
   The Kodi addon ID is `plugin.audio.radiode`; it differs from the repository name.
2. Check that the Build workflow passes. Install its ZIP on the Cube and test
   station search, favourites, playback, station switching and podcasts.
3. To enable publication, configure `REPO_SILVO_PAT` in this source repository's
   Actions secrets. It needs Contents read/write on `IkHadHonger/repository.silvo`.
   A secret configured in another repository is not automatically shared here.
4. Test changes before merging to `main`. Publish Piers automatically allocates
   a version for changed addon packages and publishes to `repository.silvo`, branch
   `cube-custom`. Manual dispatch remains available for retries.
   The workflow uses the built-in GitHub token to commit `addon.xml` to this source
   repository. That bot commit does not trigger another workflow; the current run
   rebuilds and publishes the exact versioned source commit.

There is no upstream synchronization. Automatic publication targets Piers only. AVDVPlus
is not a publication target. Existing repository addon 1.0.3 needs no version bump
solely for adding an addon to its Piers catalogue.

## Releases and recovery

The patch version is allocated automatically; document functional changes in
`changelog.txt`. You may still choose a higher version explicitly. Publication refuses to
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
