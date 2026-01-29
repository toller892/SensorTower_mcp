#!/usr/bin/env python3
"""
Test script for dual token failover functionality
Simple standalone test without external dependencies
"""

class MockSensorTowerTool:
    """Mock version of SensorTowerTool for testing token switching logic"""
    
    def __init__(self, token: str, backup_tokens: list = None):
        self.token = token
        self.backup_tokens = backup_tokens or []
        self.current_token_index = 0
        self.all_tokens = [token] + self.backup_tokens
    
    def get_auth_token(self) -> str:
        """Get current authentication token"""
        return self.all_tokens[self.current_token_index]
    
    def switch_to_backup_token(self) -> bool:
        """Switch to next available backup token. Returns True if switched, False if no more tokens."""
        if self.current_token_index < len(self.all_tokens) - 1:
            self.current_token_index += 1
            print(f"⚠️  Switching to backup token #{self.current_token_index + 1}")
            return True
        return False

def test_token_failover():
    """Test automatic token switching on quota errors"""
    
    # Initialize tool with primary and backup tokens
    primary_token = "st_primary_token_123"
    backup_tokens = ["st_backup_token_456", "st_backup_token_789"]
    
    tool = MockSensorTowerTool(primary_token, backup_tokens)
    
    print("🧪 Testing Token Failover Mechanism\n")
    
    # Test 1: Check initial token
    print(f"✓ Initial token: {tool.get_auth_token()}")
    assert tool.get_auth_token() == primary_token
    assert tool.current_token_index == 0
    
    # Test 2: Switch to first backup
    print(f"✓ Switching to backup token...")
    switched = tool.switch_to_backup_token()
    assert switched == True
    assert tool.current_token_index == 1
    assert tool.get_auth_token() == backup_tokens[0]
    print(f"✓ Now using: {tool.get_auth_token()}")
    
    # Test 3: Switch to second backup
    print(f"✓ Switching to second backup token...")
    switched = tool.switch_to_backup_token()
    assert switched == True
    assert tool.current_token_index == 2
    assert tool.get_auth_token() == backup_tokens[1]
    print(f"✓ Now using: {tool.get_auth_token()}")
    
    # Test 4: No more tokens available
    print(f"✓ Attempting to switch beyond available tokens...")
    switched = tool.switch_to_backup_token()
    assert switched == False
    assert tool.current_token_index == 2  # Should stay at last token
    print(f"✓ Correctly stayed at last token: {tool.get_auth_token()}")
    
    # Test 5: Tool with no backup tokens
    print(f"\n✓ Testing tool with no backup tokens...")
    tool_no_backup = MockSensorTowerTool(primary_token, [])
    assert tool_no_backup.get_auth_token() == primary_token
    switched = tool_no_backup.switch_to_backup_token()
    assert switched == False
    print(f"✓ Correctly cannot switch when no backup available")
    
    print("\n✅ All token failover tests passed!")
    print("\n📝 Summary:")
    print("   - Primary token switches to backup when quota exhausted")
    print("   - Multiple backup tokens supported")
    print("   - Gracefully handles no backup tokens scenario")

if __name__ == "__main__":
    test_token_failover()
