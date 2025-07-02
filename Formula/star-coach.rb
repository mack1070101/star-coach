class StarCoach < Formula
  desc "CLI tool for practicing STAR interview answers with timed sections"
  homepage "https://github.com/starcoach/star-coach"
  version "0.1.0"
  
  # For now, we'll use the local path. In production, this would be a GitHub release URL
  url "file://#{File.dirname(__FILE__)}/../"
  sha256 "placeholder" # This will be calculated when you create a release
  
  depends_on "python@3.8"
  
  def install
    # Install the Python package
    system "python3", "-m", "pip", "install", *std_pip_args, "."
    
    # Also install the standalone script as a backup
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
      STAR Coach has been installed! You can now use:
      
      # Main CLI (requires typer and rich)
      star-coach --file example.org
      
      # Standalone version (no dependencies)
      star-coach-standalone --file example.org
      
      For more information, visit: #{homepage}
    EOS
  end
end 