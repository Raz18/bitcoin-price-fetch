"""
Test script to verify the logger factory integration.

This script tests the new logger utility and ensures all modules
can properly use the centralized logging system.

Author: Senior Automation Engineer
Date: June 2025
"""

import sys
from pathlib import Path

# Add the current directory to the path for imports
sys.path.append(str(Path(__file__).parent))

def test_logger_factory():
    """Test the logger factory functionality."""
    print("🧪 Testing Logger Factory Integration")
    print("=" * 50)
    
    try:
        # Test basic logger import
        from utils import get_logger, LoggerFactory, PerformanceLogger
        print("✅ Successfully imported logger utilities")
        
        # Test logger configuration
        LoggerFactory.configure(
            log_directory=Path("test_logs"),
            log_level="INFO",
            max_file_size_mb=5,
            backup_count=3
        )
        print("✅ Logger factory configured successfully")
        
        # Test basic logger
        logger = get_logger("TestModule")
        logger.info("Test log message from TestModule")
        print("✅ Basic logger test passed")
        
        # Test performance logger
        with PerformanceLogger("test_operation") as perf:
            import time
            time.sleep(0.1)
            perf.log_metric("test_metric", 42)
            perf.log_checkpoint("halfway_point")
            time.sleep(0.1)
        print("✅ Performance logger test passed")
        
        # Test logger statistics
        stats = LoggerFactory.get_log_stats()
        print(f"✅ Logger statistics: {stats['active_loggers']} active loggers")
        
        print("\n🎉 All logger tests passed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Logger test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_config_integration():
    """Test config module integration with logger."""
    print("\n🧪 Testing Config Integration")
    print("=" * 50)
    
    try:
        from config import Config
        config = Config()
        print("✅ Config loaded with new logger system")
        
        # Test configuration validation
        config.validate()
        print("✅ Config validation passed")
        
        return True
        
    except Exception as e:
        print(f"❌ Config integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_main_app_integration():
    """Test main application integration."""
    print("\n🧪 Testing Main App Integration")
    print("=" * 50)
    
    try:
        from main import ApplicationRunner
        app = ApplicationRunner()
        print("✅ ApplicationRunner created with new logger system")
        
        # Test logger access
        app.logger.info("Test message from ApplicationRunner")
        print("✅ ApplicationRunner logger test passed")
        
        return True
        
    except Exception as e:
        print(f"❌ Main app integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def cleanup_test_files():
    """Clean up test files."""
    try:
        import shutil
        test_logs_dir = Path("test_logs")
        if test_logs_dir.exists():
            shutil.rmtree(test_logs_dir)
            print("🧹 Cleaned up test log files")
    except Exception as e:
        print(f"⚠️ Warning: Could not clean up test files: {e}")


def main():
    """Run all tests."""
    print("🪙 Bitcoin Price Tracker - Logger Integration Tests")
    print("=" * 60)
    
    test_results = []
    
    # Run tests
    test_results.append(test_logger_factory())
    test_results.append(test_config_integration())
    test_results.append(test_main_app_integration())
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(test_results)
    total = len(test_results)
    
    print(f"Tests Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Logger integration is successful.")
        success = True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        success = False
    
    # Cleanup
    cleanup_test_files()
    
    print("\n💡 Next steps:")
    if success:
        print("   - Run 'python main.py' to test the full application")
        print("   - Run 'python example_usage.py' for interactive examples")
        print("   - Check logs/ directory for application logs")
    else:
        print("   - Fix the import errors above")
        print("   - Ensure all dependencies are installed: pip install -r requirements.txt")
    
    return success


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n👋 Test interrupted by user")
        cleanup_test_files()
        sys.exit(0)
    except Exception as e:
        print(f"\n💥 Fatal error during testing: {e}")
        cleanup_test_files()
        sys.exit(1)
