# Homebrew Formula
# gthnk (c) Ian Dennis Miller
# rebuild with 'make homebrew'

class Gthnk < Formula
  desc "gthnk is a personal knowledge management system"
  homepage "https://github.com/iandennismiller/gthnk"
  url "https://files.pythonhosted.org/packages/87/46/9a746442b7c9382233250773f00428aeb9a5f31cdfa23f1130f0e2d3eb48/gthnk-0.4.2.tar.gz"
  sha256 "25968404dd291ffd9f720baa15f30fb3983b6835f4729a15ea1978e544f3439a"

  resource "alabaster" do
    url "https://files.pythonhosted.org/packages/04/cb/39ba17c43293aaddd073810691b0393143d26734a8e52ed9d65059b1108c/alabaster-0.7.6.tar.gz"
    sha256 "309d33e0282c8209f792f3527f41ec04e508ff837c61fc1906dde988a256deeb"
  end

  resource "bleach" do
    url "https://files.pythonhosted.org/packages/e0/e0/8c5cc2822d2035d64cf7b4278077a7ec1e0afde7e9051128f722ec8cd97a/bleach-1.4.3.tar.gz"
    sha256 "1293061adb5a9eebb7b260516e691785ac08cc1646c8976aeda7db9dbb1c6f4b"
  end

  resource "cssselect" do
    url "https://files.pythonhosted.org/packages/aa/e5/9ee1460d485b94a6d55732eb7ad5b6c084caf73dd6f9cb0bb7d2a78fafe8/cssselect-0.9.1.tar.gz"
    sha256 "0535a7e27014874b27ae3a4d33e8749e345bdfa62766195208b7996bf1100682"
  end

  resource "distribute" do
    url "https://files.pythonhosted.org/packages/5f/ad/1fde06877a8d7d5c9b60eff7de2d452f639916ae1d48f0b8f97bf97e570a/distribute-0.7.3.zip"
    sha256 "3dc7a8d059dcf72f0ead2fa2144a24ee0ef07dce816e8c3545d7345767138c5e"
  end

  resource "Flask" do
    url "https://files.pythonhosted.org/packages/55/8a/78e165d30f0c8bb5d57c429a30ee5749825ed461ad6c959688872643ffb3/Flask-0.11.1.tar.gz"
    sha256 "b4713f2bfb9ebc2966b8a49903ae0d3984781d5c878591cf2f7b484d28756b0e"
  end

  resource "Flask-Cache" do
    url "https://files.pythonhosted.org/packages/91/c4/f71095437bd4b691c63f240e72a20c57e2c216085cbc271f79665885d3da/Flask-Cache-0.13.1.tar.gz"
    sha256 "90126ca9bc063854ef8ee276e95d38b2b4ec8e45fd77d5751d37971ee27c7ef4"
  end

  resource "Flask-Diamond" do
    url "https://files.pythonhosted.org/packages/da/e1/7f3af4f49c87f6c8d81a7f07b0fff0c1164a9ed255b644a448ce4873c472/Flask-Diamond-0.4.6.tar.gz"
    sha256 "ee03726394ed0f70529f57d8291f6eac5b752af356a6400c772427ecb07b6068"
  end

  resource "gitdb" do
    url "https://files.pythonhosted.org/packages/e3/95/7e5d7261feb46c0539ac5e451be340ddd64d78c5118f2d893b052c76fe8c/gitdb-0.6.4.tar.gz"
    sha256 "a3ebbc27be035a2e874ed904df516e35f4a29a778a764385de09de9e0f139658"
  end

  resource "GitPython" do
    url "https://files.pythonhosted.org/packages/07/a6/87fc59935a67e26ad50cee5c731b6b133f1fb76d89028fe2d388f7349423/GitPython-1.0.1.tar.gz"
    sha256 "9c88c17bbcae2a445ff64024ef13526224f70e35e38c33416be5ceb56ca7f760"
  end

  resource "Markdown" do
    url "https://files.pythonhosted.org/packages/d4/32/642bd580c577af37b00a1eb59b0eaa996f2d11dfe394f3dd0c7a8a2de81a/Markdown-2.6.7.tar.gz"
    sha256 "daebf24846efa7ff269cfde8c41a48bb2303920c7b2c7c5e04fa82e6282d05c0"
  end

  resource "mdx-journal" do
    url "https://files.pythonhosted.org/packages/1e/0e/2aca226ea92f4227e21e32a8b5223962f2d5091e60265bb189759fa55813/mdx_journal-0.1.4.tar.gz"
    sha256 "7b7d8f011164c38e3ea2aa0de8d89b62e514155887671cd1ea894d7021afdd3e"
  end

  resource "mdx_linkify" do
    url "https://files.pythonhosted.org/packages/af/54/4425b352de6240ba50b7c8b798c21dac43d740072ffb6fd6b2ae759c9b56/mdx_linkify-0.5.tar.gz"
    sha256 "4f52f57a011ca6c3f593e298e34766a8b629e756938b60b20ff41da6fda98b34"
  end

  resource "parsedatetime" do
    url "https://files.pythonhosted.org/packages/8b/20/37822d52be72c99cad913fad0b992d982928cac882efbbc491d4b9d216a9/parsedatetime-2.1.tar.gz"
    sha256 "17c578775520c99131634e09cfca5a05ea9e1bd2a05cd06967ebece10df7af2d"
  end

  resource "poodledo" do
    url "https://files.pythonhosted.org/packages/c1/fc/2a8e5e227c5dc870734dd5f236a581e889f760272e537c3560606e130c72/poodledo-0.2.tar.gz"
    sha256 "de62fd0b6b3403ad2991b4ec7d9045c59734e9cc09c2831b07c8edb386b339fd"
  end

  resource "PyPDF2" do
    url "https://files.pythonhosted.org/packages/01/65/51461af90d6370b66327e37a7af7911db3ebada71af224cc998a85602fbc/PyPDF2-1.24.tar.gz"
    sha256 "aca40d5155524120fceaf2eb4ae054480b8a2b6ffcfa0a2e77e3e45666428c64"
  end

  resource "pyScss" do
    url "https://files.pythonhosted.org/packages/7f/76/cebba7b38a2c092bbc08d6a797bc9acf11c07c82464f05af9d524a552986/pyScss-1.2.0.post3.tar.gz"
    sha256 "f08d35992b70298453bfb7e0ada649d639f3f616730fdd16e59c6289c22b5b00"
  end

  resource "python-dateutil" do
    url "https://files.pythonhosted.org/packages/3e/f5/aad82824b369332a676a90a8c0d1e608b17e740bbb6aeeebca726f17b902/python-dateutil-2.5.3.tar.gz"
    sha256 "1408fdb07c6a1fa9997567ce3fcee6a337b39a503d80699e0f213de4aa4b32ed"
  end

  resource "requests" do
    url "https://files.pythonhosted.org/packages/0f/d0/e80371e64a7a7bafa303ea50465456e5292d9436504ce39b9619b6ba24be/requests-2.4.1.tar.gz"
    sha256 "35d890b0aaa6e09ec40d49361d823b998ced86cc7673a9ce70bbc4f986e13ad8"
  end

  resource "six" do
    url "https://files.pythonhosted.org/packages/b3/b2/238e2590826bfdd113244a40d9d3eb26918bd798fc187e2360a8367068db/six-1.10.0.tar.gz"
    sha256 "105f8d68616f8248e24bf0e9372ef04d3cc10104f1980f54d57b2ce73a5ad56a"
  end

  resource "smmap" do
    url "https://files.pythonhosted.org/packages/bc/aa/b744b3761fff1b10579df996a2d2e87f124ae07b8336e37edc89cc502f86/smmap-0.9.0.tar.gz"
    sha256 "0e2b62b497bd5f0afebc002eda4d90df9d209c30ef257e8673c90a6b5c119d62"
  end

  resource "Wand" do
    url "https://files.pythonhosted.org/packages/e8/7d/321d21be1616243c280c093064242360c2bc9af5cd35b5de4e4adc1c6fab/Wand-0.3.9.tar.gz"
    sha256 "ab44a4280688af525f9bc10af8b5f7d67e0d8244e76e4008e70337ec45fc4cb7"
  end

  include Language::Python::Virtualenv

  def install
    virtualenv_install_with_resources
  end
end
