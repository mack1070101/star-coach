class StarCoach < Formula
  desc "CLI tool for practicing STAR interview answers with timed sections"
  homepage "https://github.com/mack1070101/star-coach"
  url "https://github.com/mack1070101/star-coach/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "47333e8982f5c8cff8d3cd1199317a2e0d92e98e59f2a33a3f3f7e4e89d429ad"
  license "MIT"
  head "https://github.com/mack1070101/star-coach.git", branch: "main"
  
  depends_on "python@3.8"
  
  def install
    # Install the standalone script
    bin.install "star_coach_standalone.py" => "star-coach"
    
    # Make it executable
    chmod 0755, bin/"star-coach"
  end
  
  test do
    # Test the standalone version
    system "#{bin}/star-coach", "--help"
  end
  
  def caveats
    <<~EOS
      🌟 STAR Coach has been installed successfully!
      
      You can now use:
      
      # Practice with default empty sections
      star-coach
      
      # Practice with custom file
      star-coach --file example.org
      
      # Practice with the included example
      star-coach --file example_star.org
      
      For more information and examples, visit: #{homepage}
    EOS
  end
end 