from fastapi.middleware.cors import CORSMiddleware

def setup_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:2080"],  # 允许所有来源，你也可以指定特定的来源
        allow_credentials=True,        # 允许携带凭证（如cookies）
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )