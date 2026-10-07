import json, urllib.request

with open('.env') as f:
    for line in f:
        if line.startswith('WANDB_API_KEY='):
            key = line.split('=', 1)[1].strip()

# Check project status
query_check = """
query GetProject {
  project(entityName: "navin_hill", name: "huggingface") {
    id
    name
    totalRuns
  }
}
"""

req = urllib.request.Request(
    'https://api.wandb.ai/graphql',
    data=json.dumps({'query': query_check}).encode('utf-8'),
    headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'}
)

with urllib.request.urlopen(req) as resp:
    res = json.loads(resp.read().decode('utf-8'))
    print("Project status:", res)
    proj = res.get('data', {}).get('project')

if proj and proj.get('id'):
    # Try deleting the project
    del_mutation = """
    mutation DeleteExp($id: ID!) {
      deleteExperiment(input: {id: $id}) {
        clientMutationId
      }
    }
    """
    req_del = urllib.request.Request(
        'https://api.wandb.ai/graphql',
        data=json.dumps({'query': del_mutation, 'variables': {'id': proj['id']}}).encode('utf-8'),
        headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'}
    )
    try:
        with urllib.request.urlopen(req_del) as resp_del:
            print("Project delete result:", resp_del.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        print("Project delete HTTP error:", e.code, e.read().decode('utf-8'))
