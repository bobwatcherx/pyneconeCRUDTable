import pynecone as pc

class YtpynecrudConfig(pc.Config):
    pass

config = YtpynecrudConfig(
    app_name="ytpynecrud",
    db_url="sqlite:///pynecone.db",
    env=pc.Env.DEV,
)
