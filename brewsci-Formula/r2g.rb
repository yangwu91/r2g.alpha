# /usr/local/Homebrew/Library/Taps/brewsci/homebrew-bio/Formula/r2g.rb
class R2g < Formula
  include Language::Python::Virtualenv
  desc "A homology-based, computationally lightweight pipeline for discovering genes in the absence of an assembly"
  homepage "https://yangwu91.github.io/r2g/"
  url "https://test-files.pythonhosted.org/packages/21/6d/8c575996126e4b4ccd3ecfa340e5a5370471cf04a2212e8cf0ac81b28db9/r2g-1.0.2a0.tar.gz"
  sha256 "83acded2c5591bcc49b4022882754961413f2b3ed66b38408c86bbf88888aebd"
  license "MIT"
  head "https://github.com/yangwu91/r2g.git"

  depends_on "python@3.8"
  depends_on "sratoolkit"
  depends_on "brewsci/bio/trinity"

  resource "certifi" do
    url "https://files.pythonhosted.org/packages/40/a7/ded59fa294b85ca206082306bba75469a38ea1c7d44ea7e1d64f5443d67a/certifi-2020.6.20.tar.gz"
    sha256 "5930595817496dd21bb8dc35dad090f1c2cd0adfaf21204bf6732ca5d8ee34d3"
  end

  resource "chardet" do
    url "https://files.pythonhosted.org/packages/fc/bb/a5768c230f9ddb03acc9ef3f0d4a3cf93462473795d18e9535498c8f929d/chardet-3.0.4.tar.gz"
    sha256 "84ab92ed1c4d4f16916e05906b6b75a6c0fb5db821cc65e70cbd64a3e2a5eaae"
  end

  resource "idna" do
    url "https://files.pythonhosted.org/packages/ea/b7/e0e3c1c467636186c39925827be42f16fee389dc404ac29e930e9136be70/idna-2.10.tar.gz"
    sha256 "b307872f855b18632ce0c21c5e45be78c0ea7ae4c15c828c20788b26921eb3f6"
  end

  resource "numpy" do
    url "https://files.pythonhosted.org/packages/bf/e8/15aea783ea72e2d4e51e3ec365e8dc4a1a32c9e5eb3a6d695b0d58e67cdd/numpy-1.19.2.zip"
    sha256 "0d310730e1e793527065ad7dde736197b705d0e4c9999775f212b03c44a8484c"
  end

  resource "urllib3" do
    url "https://files.pythonhosted.org/packages/81/f4/87467aeb3afc4a6056e1fe86626d259ab97e1213b1dfec14c7cb5f538bf0/urllib3-1.25.10.tar.gz"
    sha256 "91056c15fa70756691db97756772bb1eb9678fa585d9184f24534b100dc60f4a"
  end

  resource "requests" do
    url "https://files.pythonhosted.org/packages/da/67/672b422d9daf07365259958912ba533a0ecab839d4084c487a5fe9a5405f/requests-2.24.0.tar.gz"
    sha256 "b3559a131db72c33ee969480840fff4bb6dd111de7dd27c8ee1f820f4f00231b"
  end

  resource "selenium" do
    url "https://files.pythonhosted.org/packages/ed/9c/9030520bf6ff0b4c98988448a93c04fcbd5b13cd9520074d8ed53569ccfe/selenium-3.141.0.tar.gz"
    sha256 "deaf32b60ad91a4611b98d8002757f29e6f2c2d5fcaf202e1c9ad06d6772300d"
  end

  def install
    virtualenv_install_with_resources
  end

  test do
    assert_match "usage", shell_output("#{bin}/r2g --help")
  end
end

# icu4c is keg-only, which means it was not symlinked into /usr/local,
# because macOS provides libicucore.dylib (but nothing else).
#
# If you need to have icu4c first in your PATH run:
#   echo 'export PATH="/usr/local/opt/icu4c/bin:$PATH"' >> /Users/wuyang/.bash_profile
#   echo 'export PATH="/usr/local/opt/icu4c/sbin:$PATH"' >> /Users/wuyang/.bash_profile
#
# For compilers to find icu4c you may need to set:
#   export LDFLAGS="-L/usr/local/opt/icu4c/lib"
#   export CPPFLAGS="-I/usr/local/opt/icu4c/include"


