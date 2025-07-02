class StarCoach < Formula
  desc "CLI tool for practicing STAR interview answers with timed sections"
  homepage "https://github.com/mack1070101/star-coach"
  url "https://github.com/mack1070101/star-coach/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "PLACEHOLDER_SHA256" # Replace with actual SHA256 when you create a release
  license "MIT"
  head "https://github.com/mack1070101/star-coach.git", branch: "main"
  
  depends_on "python@3.8"
  
  def install
    # Install the Python package
    system "python3", "-m", "pip", "install", *std_pip_args, "."
    
    # Also install the standalone script as a backup option
    bin.install "star_coach_standalone.py" => "star-coach-standalone"
  end
  
  test do
    # Test the main CLI
    system "#{bin}/star-coach", "--help"
    
    # Test the standalone version
    system "#{bin}/star-coach-standalone", "--help"
  end
  
  def caveats
    <<~EOS
      🌟 STAR Coach has been installed successfully!
      
      You can now use:
      
      # Main CLI (with beautiful progress bars)
      star-coach --file example.org
      
      # Standalone version (no external dependencies)
      star-coach-standalone --file example.org
      
      # Practice with default empty sections
      star-coach
      
      For more information and examples, visit: #{homepage}
    EOS
  end
end 