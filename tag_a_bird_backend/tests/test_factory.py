from tag_a_bird_backend import config, create_app

def test_config():
    assert create_app(config.TestConfig).testing
