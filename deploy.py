"""
Enterprise Math Tutor Deployment Script
Handles complete deployment of the enterprise system
"""

import os
import subprocess
import sys
import json
import time
from pathlib import Path
import argparse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnterpriseMathTutorDeployment:
    """Deployment manager for the enterprise math tutor system"""
    
    def __init__(self):
        self.root_dir = Path(__file__).parent.parent
        self.backend_dir = self.root_dir / "backend"
        self.frontend_dir = self.root_dir / "frontend"
        self.mcp_dir = self.root_dir / "mcp_server"
        
    def check_prerequisites(self):
        """Check system prerequisites"""
        print("🔍 Checking Prerequisites...")
        
        # Check Python version
        python_version = sys.version_info
        if python_version.major < 3 or python_version.minor < 8:
            print(f"❌ Python 3.8+ required, found {python_version.major}.{python_version.minor}")
            return False
        print(f"✅ Python {python_version.major}.{python_version.minor} is compatible")
        
        # Check Node.js for frontend (if available)
        try:
            result = subprocess.run(['node', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Node.js available: {result.stdout.strip()}")
            else:
                print("⚠️  Node.js not found - frontend will need manual setup")
        except FileNotFoundError:
            print("⚠️  Node.js not found - frontend will need manual setup")
        
        return True
    
    def setup_environment(self):
        """Set up environment file"""
        print("🔧 Setting up Environment Configuration...")
        
        env_template = self.backend_dir / ".env.template"
        env_file = self.backend_dir / ".env"
        
        if not env_template.exists():
            print(f"❌ Environment template not found: {env_template}")
            return False
        
        if env_file.exists():
            print("⚠️  .env file already exists - skipping environment setup")
            return True
        
        # Copy template
        try:
            with open(env_template, 'r') as template:
                content = template.read()
            
            with open(env_file, 'w') as env:
                env.write(content)
            
            print(f"✅ Environment file created: {env_file}")
            print("📝 Please edit .env file with your actual API keys and credentials")
            return True
            
        except Exception as e:
            print(f"❌ Failed to create environment file: {e}")
            return False
    
    def install_backend_dependencies(self):
        """Install backend Python dependencies"""
        print("📦 Installing Backend Dependencies...")
        
        requirements_file = self.backend_dir / "requirements.txt"
        if not requirements_file.exists():
            print(f"❌ Requirements file not found: {requirements_file}")
            return False
        
        try:
            # Change to backend directory
            os.chdir(self.backend_dir)
            
            # Install dependencies
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Backend dependencies installed successfully")
                return True
            else:
                print(f"❌ Failed to install dependencies: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Failed to install backend dependencies: {e}")
            return False
    
    def install_frontend_dependencies(self):
        """Install frontend Node.js dependencies"""
        print("🎨 Installing Frontend Dependencies...")
        
        package_json = self.frontend_dir / "package.json"
        if not package_json.exists():
            print(f"❌ Package.json not found: {package_json}")
            return False
        
        try:
            # Check if npm is available
            subprocess.run(['npm', '--version'], capture_output=True, check=True)
            
            # Change to frontend directory
            os.chdir(self.frontend_dir)
            
            # Install dependencies
            result = subprocess.run(['npm', 'install'], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Frontend dependencies installed successfully")
                return True
            else:
                print(f"❌ Failed to install frontend dependencies: {result.stderr}")
                return False
                
        except subprocess.CalledProcessError:
            print("⚠️  npm not available - frontend dependencies not installed")
            return False
        except Exception as e:
            print(f"❌ Failed to install frontend dependencies: {e}")
            return False
    
    def run_integration_test(self):
        """Run the integration test"""
        print("🧪 Running Integration Tests...")
        
        test_script = self.backend_dir / "enterprise_integration_test.py"
        if not test_script.exists():
            print(f"❌ Integration test script not found: {test_script}")
            return False
        
        try:
            # Change to backend directory
            os.chdir(self.backend_dir)
            
            # Run integration test
            result = subprocess.run([
                sys.executable, "enterprise_integration_test.py"
            ], capture_output=True, text=True)
            
            print("📊 Integration test output:")
            print(result.stdout)
            
            if result.stderr:
                print("⚠️  Integration test warnings/errors:")
                print(result.stderr)
            
            # Check if test report exists
            report_file = self.backend_dir / "integration_test_report.json"
            if report_file.exists():
                with open(report_file, 'r') as f:
                    test_results = json.load(f)
                
                overall_status = test_results.get("overall_status", "unknown")
                if overall_status == "pass":
                    print("✅ All integration tests passed")
                    return True
                elif overall_status == "partial_pass":
                    print("⚠️  Some integration tests passed - review report")
                    return True
                else:
                    print("❌ Integration tests failed - check report")
                    return False
            else:
                print("⚠️  Integration test completed but no report generated")
                return result.returncode == 0
                
        except Exception as e:
            print(f"❌ Failed to run integration tests: {e}")
            return False
    
    def create_startup_scripts(self):
        """Create startup scripts"""
        print("📜 Creating Startup Scripts...")
        
        # Backend startup script
        backend_script = self.backend_dir / "start_backend.py"
        backend_content = '''#!/usr/bin/env python3
"""
Backend Startup Script
"""
import os
import uvicorn
from pathlib import Path

if __name__ == "__main__":
    # Load environment
    from dotenv import load_dotenv
    load_dotenv()
    
    # Start the FastAPI server
    print("🚀 Starting Enterprise Math Tutor Backend...")
    uvicorn.run(
        "main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", "8000")),
        reload=os.getenv("DEBUG", "false").lower() == "true",
        log_level="info"
    )
'''
        
        with open(backend_script, 'w') as f:
            f.write(backend_content)
        
        # Frontend startup script (if Node.js available)
        frontend_script = self.frontend_dir / "start_frontend.js"
        frontend_content = '''// Frontend Startup Script
const { spawn } = require('child_process');

console.log('🎨 Starting Enterprise Math Tutor Frontend...');

const frontend = spawn('npm', ['start'], { stdio: 'inherit' });

frontend.on('close', (code) => {
  console.log(`Frontend process exited with code ${code}`);
});
'''
        
        if (self.frontend_dir / "package.json").exists():
            with open(frontend_script, 'w') as f:
                f.write(frontend_content)
        
        # Make scripts executable (Unix-like systems)
        try:
            os.chmod(backend_script, 0o755)
            if frontend_script.exists():
                os.chmod(frontend_script, 0o755)
        except:
            pass  # Windows doesn't need chmod
        
        print("✅ Startup scripts created")
        return True
    
    def deploy(self, skip_tests=False, skip_frontend=False):
        """Complete deployment process"""
        print("🚀 ENTERPRISE MATH TUTOR DEPLOYMENT")
        print("=" * 50)
        
        deployment_steps = [
            ("Prerequisites", self.check_prerequisites),
            ("Environment Setup", self.setup_environment),
            ("Backend Dependencies", self.install_backend_dependencies),
        ]
        
        if not skip_frontend:
            deployment_steps.append(("Frontend Dependencies", self.install_frontend_dependencies))
        
        deployment_steps.extend([
            ("Startup Scripts", self.create_startup_scripts),
        ])
        
        if not skip_tests:
            deployment_steps.append(("Integration Tests", self.run_integration_test))
        
        failed_steps = []
        
        for step_name, step_function in deployment_steps:
            print(f"\n🔄 {step_name}...")
            try:
                if not step_function():
                    failed_steps.append(step_name)
                    print(f"❌ {step_name} failed")
                else:
                    print(f"✅ {step_name} completed")
            except Exception as e:
                failed_steps.append(step_name)
                print(f"❌ {step_name} failed with error: {e}")
        
        print("\n" + "=" * 50)
        print("📋 DEPLOYMENT SUMMARY")
        print("=" * 50)
        
        if not failed_steps:
            print("🎉 DEPLOYMENT SUCCESSFUL!")
            print("\nNext steps:")
            print("1. Edit the .env file with your API keys")
            print("2. Start the backend: python start_backend.py")
            if not skip_frontend:
                print("3. Start the frontend: npm start (in frontend directory)")
            print("4. Access the application at http://localhost:3000")
            
        else:
            print(f"⚠️  DEPLOYMENT PARTIALLY SUCCESSFUL")
            print(f"Failed steps: {', '.join(failed_steps)}")
            print("\nPlease resolve the failed steps before starting the application.")
        
        print("=" * 50)
        
        # Create deployment summary
        deployment_summary = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "success": len(failed_steps) == 0,
            "failed_steps": failed_steps,
            "next_steps": [
                "Edit .env file with API keys",
                "Start backend with: python start_backend.py",
                "Start frontend with: npm start (if frontend installed)",
                "Access at http://localhost:3000"
            ]
        }
        
        with open(self.root_dir / "deployment_summary.json", 'w') as f:
            json.dump(deployment_summary, f, indent=2)
        
        return len(failed_steps) == 0

def main():
    parser = argparse.ArgumentParser(description="Deploy Enterprise Math Tutor")
    parser.add_argument("--skip-tests", action="store_true", help="Skip integration tests")
    parser.add_argument("--skip-frontend", action="store_true", help="Skip frontend setup")
    
    args = parser.parse_args()
    
    deployer = EnterpriseMathTutorDeployment()
    success = deployer.deploy(skip_tests=args.skip_tests, skip_frontend=args.skip_frontend)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
