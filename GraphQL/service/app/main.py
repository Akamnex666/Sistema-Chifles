from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
import os
from dotenv import load_dotenv

from infrastructure.http_client import RESTClient
from interface.graphql.schema import schema, get_context
from strawberry.fastapi import GraphQLRouter

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# Load .env from the service directory (GraphQL/service/.env)
load_dotenv(os.path.join(BASE_DIR, '.env'))

API_URL = os.getenv('API_URL', 'http://127.0.0.1:3000/chifles')
PORT = int(os.getenv('PORT', '8001'))

def create_app() -> FastAPI:
    app = FastAPI(title="Sistema-Chifles - GraphQL Reports")

    @app.on_event('startup')
    async def startup():
        app.state.rest = RESTClient(base_url=API_URL)

    @app.on_event('shutdown')
    async def shutdown():
        client = getattr(app.state, 'rest', None)
        if client:
            await client.close()
        

    @app.get('/health')
    async def health():
        return JSONResponse({'status': 'ok'})

    graphql_app = GraphQLRouter(
        schema,
        context_getter=get_context,
        graphiql=True 
    )

    app.include_router(graphql_app, prefix="/graphql")

    @app.middleware("http")
    async def block_post_graphql(request: Request, call_next):
        # Allow POST only from localhost so GraphiQL (introspection) works locally;
        # block POST from remote clients.
        if request.url.path.startswith("/graphql") and request.method.upper() == "POST":
            client_host = None
            if request.client:
                client_host = request.client.host
            # permit localhost IPv4/IPv6 and hostname
            if client_host in ("127.0.0.1", "::1", "localhost"):
                return await call_next(request)
            return JSONResponse({"detail": "POST not allowed on this GraphQL endpoint. Use GET/GraphiQL."}, status_code=405)
        return await call_next(request)

    return app


app = create_app()

if __name__ == '__main__':
    uvicorn.run('app.main:app', host='127.0.0.1', port=PORT, reload=True)
