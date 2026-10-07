import os, json, urllib.request

with open('.env') as f:
    for line in f:
        if line.startswith('WANDB_API_KEY='):
            key = line.split('=', 1)[1].strip()

gql = '''query ProjectRuns {
  project(entityName: "navin_hill", name: "copyright") {
    runs(first: 5, order: "-createdAt") {
      edges {
        node {
          name
          id
          state
          createdAt
          heartbeatAt
          summaryMetrics
        }
      }
    }
  }
}'''

req = urllib.request.Request(
    'https://api.wandb.ai/graphql',
    data=json.dumps({'query': gql}).encode('utf-8'),
    headers={
        'Authorization': f'Bearer {key}',
        'Content-Type': 'application/json'
    }
)

try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        runs = data.get('data', {}).get('project', {}).get('runs', {}).get('edges', [])
        print(f'Runs found in navin_hill/copyright: {len(runs)}')
        for r in runs:
            node = r['node']
            print('Run:', node.get('name'), '| State:', node.get('state'), '| Created:', node.get('createdAt'))
            print('  Summary:', node.get('summaryMetrics'))
except Exception as e:
    print('Error querying W&B:', e)
