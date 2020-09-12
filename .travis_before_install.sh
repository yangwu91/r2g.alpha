#!/bin/bash

set -e
set -u

brew tap brewsci/bio
cp ./brewsci-Formula/r2g.rb /usr/local/Homebrew/Library/Taps/brewsci/homebrew-bio/Formula/
brew install r2g

mkdir -p "${HOME}"/.ncbi
cat > "${HOME}"/.ncbi/user-settings.mkfg <<_EOF
## auto-generated configuration file - DO NOT EDIT ##

/LIBS/GUID = "$(uuidgen)"
/config/default = "false"
/repository/user/ad/public/apps/file/volumes/flatAd = "."
/repository/user/ad/public/apps/refseq/volumes/refseqAd = "."
/repository/user/ad/public/apps/sra/volumes/sraAd = "."
/repository/user/ad/public/apps/sraPileup/volumes/ad = "."
/repository/user/ad/public/apps/sraRealign/volumes/ad = "."
/repository/user/ad/public/root = "."
/repository/user/default-path = "${HOME}/ncbi"

_EOF
