"""Test different configurations."""

from app import create_app
from config import DevelopmentConfig, TestingConfig, ProductionConfig


def test_development_config():
    """Test development configuration."""
    app = create_app("config.DevelopmentConfig")
    assert app.config['DEBUG'] is True
    assert app.config['TESTING'] is False
    print("✓ Development config: DEBUG =", app.config['DEBUG'])


def test_testing_config():
    """Test testing configuration."""
    app = create_app("config.TestingConfig")
    assert app.config['TESTING'] is True
    assert app.config['DEBUG'] is True
    print("✓ Testing config: TESTING =", app.config['TESTING'])


def test_production_config():
    """Test production configuration."""
    app = create_app("config.ProductionConfig")
    assert app.config['DEBUG'] is False
    assert app.config['TESTING'] is False
    print("✓ Production config: DEBUG =", app.config['DEBUG'])


def test_default_config():
    """Test default configuration."""
    app = create_app()  # Should use DevelopmentConfig by default
    assert app.config['DEBUG'] is True
    print("✓ Default config: Uses DevelopmentConfig")


if __name__ == '__main__':
    print("Testing different configurations...\n")
    test_development_config()
    test_testing_config()
    test_production_config()
    test_default_config()
    print("\n✅ All configuration tests passed!")