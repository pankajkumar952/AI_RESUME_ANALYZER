"""Utility functions for webdriver setup and management"""
import os
import sys
import platform
import tempfile
import subprocess
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Try to import various webdriver managers with fallbacks
try:
    from webdriver_manager.chrome import ChromeDriverManager
    from webdriver_manager.core.utils import ChromeType
    webdriver_manager_available = True
except ImportError:
    webdriver_manager_available = False

try:
    import chromedriver_autoinstaller
    autoinstaller_available = True
except ImportError:
    autoinstaller_available = False

def get_chrome_version():
    """Get the installed Chrome/Chromium version"""
    system = platform.system()
    
    if system == "Windows":
        # Windows-specific Chrome detection
        try:
            # Try to find Chrome in Program Files
            chrome_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe")
            ]
            
            for path in chrome_paths:
                if os.path.exists(path):
                    try:
                        # Try using registry/wmic to get version
                        output = subprocess.check_output(
                            ['wmic', 'datafile', 'where', f'name="{path.replace("\\", "\\\\")}"', 'get', 'Version', '/value'],
                            stderr=subprocess.STDOUT
                        )
                        version_str = output.decode('utf-8').strip()
                        if "Version=" in version_str:
                            version = version_str.split('=')[1].split('.')[0]
                            return version
                    except:
                        # Try alternative method
                        try:
                            output = subprocess.check_output([path, '--version'], stderr=subprocess.STDOUT)
                            version = output.decode('utf-8').strip().split()[-1].split('.')[0]
                            return version
                        except:
                            pass
        except Exception:
            # Silently fail and continue with default
            pass
    else:
        # Linux/Mac detection
        try:
            # Try different Chrome/Chromium binaries
            for binary in ['/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser']:
                if os.path.exists(binary):
                    version = subprocess.check_output([binary, '--version'], stderr=subprocess.STDOUT)
                    version = version.decode('utf-8').strip().split()[-1].split('.')[0]
                    return version
        except Exception:
            # Silently fail and continue with default
            pass
    
    # Default to latest if all else fails
    return "120"

def run_setup_script():
    """Run the setup_chromedriver.py script to install the correct chromedriver"""
    try:
        # Get the path to the setup script
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        setup_script = os.path.join(script_dir, "setup_chromedriver.py")
        
        if os.path.exists(setup_script):
            st.info("Running chromedriver setup script...")
            result = subprocess.run([sys.executable, setup_script], 
                                   capture_output=True, text=True)
            
            if result.returncode == 0:
                st.success("Chromedriver setup completed successfully!")
                # Extract the chromedriver path from the output
                for line in result.stdout.split('\n'):
                    if "Chromedriver path:" in line:
                        chromedriver_path = line.split("Chromedriver path:")[1].strip()
                        return chromedriver_path
            else:
                st.warning(f"Chromedriver setup failed: {result.stderr}")
        else:
            st.warning(f"Setup script not found at {setup_script}")
    except Exception as e:
        st.warning(f"Error running setup script: {str(e)}")
    
    return None

def get_chromedriver_path():
    """Get the path to the chromedriver executable based on the platform"""
    system = platform.system()
    
    if system == "Windows":
        # Check in LocalAppData
        local_app_data = os.environ.get('LOCALAPPDATA', '')
        if local_app_data:
            chromedriver_path = os.path.join(local_app_data, "ChromeDriver", "chromedriver.exe")
            if os.path.exists(chromedriver_path):
                return chromedriver_path
    else:
        # Check in ~/.chromedriver
        home_dir = os.path.expanduser("~")
        chromedriver_path = os.path.join(home_dir, ".chromedriver", "chromedriver")
        if os.path.exists(chromedriver_path):
            return chromedriver_path
    
    return None

def setup_webdriver():
    """
    Set up and configure Chrome webdriver with multiple fallback options
    
    Returns:
        webdriver.Chrome or None: Configured Chrome webdriver or None if setup fails
    """
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    
    # Method 1: Try direct initialization first since it's working
    try:
        driver = webdriver.Chrome(options=options)
        st.success("Chrome webdriver initialized successfully!")
        return driver
    except Exception:
        # If direct initialization fails, try other methods
        pass
    
    # Method 2: Check if we already have a chromedriver installed
    chromedriver_path = get_chromedriver_path()
    if chromedriver_path:
        try:
            service = Service(executable_path=chromedriver_path)
            driver = webdriver.Chrome(service=service, options=options)
            return driver
        except Exception:
            # Silently fail and continue with other methods
            pass
    
    # Method 3: Try using webdriver-manager
    if webdriver_manager_available:
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            return driver
        except Exception:
            # Silently fail and continue with other methods
            pass
    
    # Method 4: Try platform-specific approaches
    system = platform.system()
    if system == "Windows":
        try:
            # Try with Chrome binary path
            chrome_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe")
            ]
            
            for path in chrome_paths:
                if os.path.exists(path):
                    options.binary_location = path
                    try:
                        driver = webdriver.Chrome(options=options)
                        return driver
                    except Exception:
                        continue
        except Exception:
            # Silently fail and continue with other methods
            pass
    elif system == "Linux":
        try:
            # Try with Chromium binary path
            options.binary_location = "/usr/bin/chromium"
            try:
                driver = webdriver.Chrome(options=options)
                return driver
            except Exception:
                pass
                
            # Try with Google Chrome binary path
            options.binary_location = "/usr/bin/google-chrome"
            try:
                driver = webdriver.Chrome(options=options)
                return driver
            except Exception:
                pass
        except Exception:
            # Silently fail and continue with other methods
            pass
    
    # All methods failed
    st.error("Failed to initialize Chrome webdriver. Please make sure Chrome is installed.")
    return None 