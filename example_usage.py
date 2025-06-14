"""
Example Usage Scripts for Bitcoin Price Tracker

Professional examples demonstrating different use cases and deployment scenarios.

Author: Senior Automation Engineer
Date: June 2025
"""

import asyncio
import sys
from pathlib import Path

# Add the current directory to the path for imports
sys.path.append(str(Path(__file__).parent))

from config import Config, ConfigurationError
from business_logic import BitcoinPriceOrchestrator
from utils import get_logger, LoggerFactory

'''
async def example_quick_test():
    """Quick test - collect price data for 3 minutes and generate reports."""
    print("\n" + "="*60)
    print("🚀 QUICK TEST EXAMPLE (3 minutes)")
    print("="*60)
    
    try:
        # Initialize configuration
        config = Config()
        
        # Override duration for quick test
        config.tracking.tracking_duration_minutes = 3
        config.tracking.enable_email_reports = False
        
        print(f"✅ Configuration loaded successfully")
        print(f"📊 Collection interval: {config.tracking.collection_interval_seconds} seconds")
        print(f"⏱️  Test duration: {config.tracking.tracking_duration_minutes} minutes")
        
        # Create and run orchestrator
        orchestrator = BitcoinPriceOrchestrator(config)
        await orchestrator.initialize()
        
        print("\n🔄 Starting price collection...")
        await orchestrator.execute_tracking_cycle()
        
        print("\n✅ Quick test completed successfully!")
        print("📁 Check the following files:")
        print(f"   - {config.data.json_file_path}")
        print(f"   - data/charts/ (for generated charts)")
        print(f"   - logs/application.log")
        
    except Exception as e:
        print(f"❌ Quick test failed: {e}")
        return False
    
    return True


async def example_full_hour_with_email():
    """Full example - collect for 1 hour and send email report."""
    print("\n" + "="*60)
    print("📧 FULL HOUR WITH EMAIL EXAMPLE")
    print("="*60)
    
    try:
        # Initialize configuration
        config = Config()
        
        # Check email configuration
        if not config.email.sender_email or not config.email.recipient_email:
            print("❌ Email configuration incomplete!")
            print("📝 Please update your .env file with email settings:")
            print("   - SENDER_EMAIL=your-email@gmail.com")
            print("   - SENDER_PASSWORD=your-app-password")
            print("   - RECIPIENT_EMAIL=recipient@gmail.com")
            print("\n💡 For Gmail users:")
            print("   1. Enable 2-Factor Authentication")
            print("   2. Generate an App Password (not your regular password)")
            print("   3. Use the App Password in SENDER_PASSWORD")
            return False
        
        # Enable email reports
        config.tracking.enable_email_reports = True
        config.tracking.tracking_duration_minutes = 60
        
        print(f"✅ Configuration loaded successfully")
        print(f"📧 Email reports: ENABLED")
        print(f"📨 Sender: {config.email.sender_email}")
        print(f"📬 Recipient: {config.email.recipient_email}")
        print(f"⏱️  Duration: {config.tracking.tracking_duration_minutes} minutes")
        
        # Create and run orchestrator
        orchestrator = BitcoinPriceOrchestrator(config)
        await orchestrator.initialize()
        
        print("\n🔄 Starting full tracking cycle with email reporting...")
        print("⚠️  This will take 1 hour to complete!")
        
        await orchestrator.execute_tracking_cycle()
        
        print("\n✅ Full tracking cycle completed!")
        print("📧 Email report should have been sent")
        
    except ConfigurationError as e:
        print(f"❌ Configuration error: {e}")
        return False
    except Exception as e:
        print(f"❌ Full tracking failed: {e}")
        return False
    
    return True


async def example_custom_duration():
    """Custom duration example - collect for 5 minutes with detailed analysis."""
    print("\n" + "="*60)
    print("⚙️  CUSTOM DURATION EXAMPLE (5 minutes)")
    print("="*60)
    
    try:
        # Initialize configuration
        config = Config()
        
        # Customize settings
        config.tracking.tracking_duration_minutes = 5
        config.tracking.enable_email_reports = False
        config.tracking.enable_graph_generation = True
        
        print(f"✅ Configuration customized:")
        print(f"   - Duration: {config.tracking.tracking_duration_minutes} minutes")
        print(f"   - Email reports: {config.tracking.enable_email_reports}")
        print(f"   - Graph generation: {config.tracking.enable_graph_generation}")
        
        # Create and run orchestrator
        orchestrator = BitcoinPriceOrchestrator(config)
        await orchestrator.initialize()
        
        print("\n🔄 Starting custom tracking cycle...")
        await orchestrator.execute_tracking_cycle()
        
        print("\n✅ Custom duration tracking completed!")
        
    except Exception as e:
        print(f"❌ Custom tracking failed: {e}")
        return False
    
    return True


async def example_configuration_test():
    """Test and validate configuration without running tracking."""
    print("\n" + "="*60)
    print("🔧 CONFIGURATION TEST EXAMPLE")
    print("="*60)
    
    try:
        # Initialize configuration
        config = Config()
        
        print("📋 Configuration Summary:")
        print("="*40)
        
        # Display configuration summary
        summary = config.get_summary()
        
        for section, settings in summary.items():
            print(f"\n📁 {section.upper()}:")
            for key, value in settings.items():
                print(f"   {key}: {value}")
        
        # Validate configuration
        print("\n🔍 Validating configuration...")
        config.validate()
        print("✅ Configuration validation passed!")
        
        # Test API connectivity
        print("\n🌐 Testing API connectivity...")
        from api_handler import BitcoinAPIHandler
        import logging
        
        logger = logging.getLogger("Test")
        api_handler = BitcoinAPIHandler(config.api, logger)
        
        health_ok = await api_handler.health_check()
        if health_ok:
            print("✅ API connectivity test passed!")
        else:
            print("❌ API connectivity test failed!")
        
        await api_handler.close()
        
        # Test email configuration if provided
        if config.email.sender_email and config.tracking.enable_email_reports:
            print("\n📧 Testing email configuration...")
            from email_sender import EmailSender
            
            email_sender = EmailSender(config.email, logger)
            email_ok = await email_sender.validate_configuration()
            
            if email_ok:
                print("✅ Email configuration test passed!")
                
                # Optionally send test email
                response = input("   Send test email? (y/N): ").strip().lower()
                if response == 'y':
                    test_sent = await email_sender.send_test_email()
                    if test_sent:
                        print("✅ Test email sent successfully!")
                    else:
                        print("❌ Test email failed!")
            else:
                print("❌ Email configuration test failed!")
            
            await email_sender.close()
        
        print("\n✅ Configuration test completed!")
        return True
        
    except ConfigurationError as e:
        print(f"❌ Configuration error: {e}")
        return False
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False


async def main():
    """Main function to run example scenarios."""
    print("🪙 Bitcoin Price Tracker - Professional Examples")
    print("=" * 60)
    print("Choose an example to run:")
    print()
    print("1. 🚀 Quick Test (3 minutes)")
    print("2. 📧 Full Hour with Email Report")
    print("3. ⚙️  Custom Duration (5 minutes)")
    print("4. 🔧 Configuration Test")
    print("5. 📊 Performance Benchmark")
    print("6. ❌ Exit")
    print()
    
    while True:
        try:
            choice = input("👉 Select option (1-6): ").strip()
            
            if choice == '1':
                await example_quick_test()
                break
            elif choice == '2':
                await example_full_hour_with_email()
                break
            elif choice == '3':
                await example_custom_duration()
                break
            elif choice == '4':
                await example_configuration_test()
                break
            elif choice == '5':
                await example_performance_benchmark()
                break
            elif choice == '6':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please select 1-6.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Exiting...")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            break


async def example_performance_benchmark():
    """Performance benchmark - test API response times and system performance."""
    print("\n" + "="*60)
    print("📊 PERFORMANCE BENCHMARK EXAMPLE")
    print("="*60)
    
    try:
        from api_handler import BitcoinAPIHandler
        from datetime import datetime
        import statistics
        import logging
        
        # Setup
        config = Config()
        logger = logging.getLogger("Benchmark")
        api_handler = BitcoinAPIHandler(config.api, logger)
        
        print("🔄 Running performance benchmark...")
        print("📡 Testing API response times (10 requests)...")
        
        response_times = []
        successful_requests = 0
        
        for i in range(10):
            start_time = datetime.now()
            price = await api_handler.fetch_bitcoin_price()
            end_time = datetime.now()
            
            response_time = (end_time - start_time).total_seconds() * 1000  # ms
            response_times.append(response_time)
            
            if price is not None:
                successful_requests += 1
                print(f"   Request {i+1}: {response_time:.1f}ms - ${price:,.2f}")
            else:
                print(f"   Request {i+1}: {response_time:.1f}ms - FAILED")
        
        # Calculate statistics
        if response_times:
            avg_response = statistics.mean(response_times)
            min_response = min(response_times)
            max_response = max(response_times)
            success_rate = (successful_requests / 10) * 100
            
            print("\n📈 Performance Results:")
            print(f"   Average Response Time: {avg_response:.1f}ms")
            print(f"   Minimum Response Time: {min_response:.1f}ms")
            print(f"   Maximum Response Time: {max_response:.1f}ms")
            print(f"   Success Rate: {success_rate:.1f}%")
            
            # Performance evaluation
            if avg_response < 1000:
                print("✅ Excellent API performance!")
            elif avg_response < 3000:
                print("✅ Good API performance")
            else:
                print("⚠️  Slow API performance detected")
        
        await api_handler.close()
        
        print("\n✅ Performance benchmark completed!")
        return True
        
    except Exception as e:
        print(f"❌ Performance benchmark failed: {e}")
        return False


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Application terminated by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)
'''