# Deploy Hooks – Render Docs

**Source**: [https://render.com/docs/deploy-hooks](https://render.com/docs/deploy-hooks)  
**Style Profile**: Direct cloud primitives, clear curl/webhook examples, pragmatic operations

---

**Deploy hooks** enable you to trigger an on-demand deploy of your Render service with a single HTTP request. Use deploy hooks with:

  * CI/CD environments like GitHub Actions (see an example)
  * Image-backed services (to trigger a deploy when a new image is available)
  * Headless CMS systems like [Contentful](https://www.contentful.com/developers/docs/concepts/webhooks/) (to trigger a deploy when content changes)

**Looking for webhooks?** See [this article](/docs/webhooks).

## Triggering a deploy

Each service has a secret **deploy hook URL** , available from its **Settings** tab in the [Render Dashboard](https://dashboard.render.com):

**Your deploy hook URL is a secret!**

Provide the URL only to people and systems you trust to trigger deploys. If you believe a deploy hook URL has been compromised, replace it by clicking **Regenerate Hook**.

To trigger a deploy, send a basic `GET` or `POST` request to your service's deploy hook URL (no special headers required):

### Response format

**On success,** Render responds with one of the following HTTP codes:

Response code| Description  
---|---  
**200 OK** |  The deploy has started. The response body is a JSON object that includes the new deploy's ID: You can get more details about the deploy by passing this ID to the Render API's [Retrieve deploy](https://api-docs.render.com/reference/retrieve-deploy) endpoint.  
**202 Accepted** |  A different deploy is already in progress for this service. Render will start a new deploy after the current one completes. In this case, the response body does _not_ include a deploy ID. This can only occur in workspaces with their [overlapping deploy policy](/docs/deploys#handling-overlapping-deploys) set to **Wait**.  
  
**On failure,** in most cases Render responds with one of the following HTTP codes:

Response code| Description  
---|---  
**400 Bad Request** |  Most commonly, the deploy hook URL included an invalid `imgURL` or `ref` query parameter. For details, see Deploying from an image registry and [Deploying a specific commit](/docs/deploys#deploying-a-specific-commit).  
**401 Unauthorized** |  The deploy hook URL's `key` query parameter was invalid or missing. This is commonly because the triggering system was not updated with the latest deploy hook URL after it was regenerated in the Render Dashboard.  
**404 Not Found** |  Most commonly one of the following:

  * No service with the URL's specified ID was found.
  * The commit SHA specified in the `ref` query parameter was not found in the service's linked repository.

  
**405 Method Not Allowed** |  The request used an HTTP method besides `GET` or `POST`.  
**409 Conflict** |  The service is suspended or your workspace is otherwise unable to trigger deploys for it.  
  
## Deploying a specific Git commit

You can specify a commit SHA to deploy by appending the `ref` query parameter to your deploy hook URL. For details, see [Deploying a specific commit](/docs/deploys#deploying-a-specific-commit).

## Deploying from an image registry

[Image-backed services](/docs/deploying-an-image) on Render pull and deploy a prebuilt Docker image from an external registry. These services do _not_ automatically redeploy if a new image is pushed to the registry. You can use a deploy hook to trigger a deploy whenever an updated image is available.

To deploy a specific tag or digest, append the `imgURL` query parameter to your deploy hook URL:

If you _don't_ provide this parameter, Render uses whichever tag or digest you've specified in the service's settings.

All components of `imgURL` _besides_ the tag or digest must match your service's default image URL. Otherwise, Render rejects the deploy request.

## Using with GitHub Actions

You might want to trigger a service deploy from your CI/CD environment whenever certain conditions are met (such as when all of your tests pass). Let's set this up using deploy hooks and [GitHub Actions](https://docs.github.com/en/actions/learn-github-actions/understanding-github-actions).

### 1\. Create a repository secret

Deploy hook URLs are secret values, so we need to make sure to [store ours as a secret](https://docs.github.com/en/actions/reference/encrypted-secrets) in our GitHub repo:

  1. Go to your GitHub repo's **Settings** page.

  2. Click **Secrets and variables > Actions**.

  3. Click **New repository secret**. Create a secret with the name `RENDER_DEPLOY_HOOK_URL` and provide your deploy hook URL as the value:

### 2\. Add a GitHub workflow

Now that we've added our deploy hook URL, let's create a GitHub workflow that uses it:

  1. Create a `.github/workflows` directory in your repo if it doesn't already exist. GitHub Actions automatically detects and runs any workflows defined in this folder.
  2. Add a YAML file to this directory to represent your new workflow. The example below uses the file path `.github/workflows/ci.yml`.
  3. Define logic in your workflow to trigger a deploy after any prerequisite steps succeed. See the example.
  4. Commit all of your changes.

#### Example workflow

This example workflow defines a job named `ci` that includes two steps (`Test` and `Deploy`). The workflow runs whenever any pull request is opened against `main`, or when commits are pushed to `main`.

  1. The `Test` step runs the repo's defined unit tests.
  2. The `Deploy` step executes a `curl` request to our deploy hook URL _only if_ the current branch is `main` _and_ the `Test` step succeeded.

Copy page

###### [Deploy Hooks](/docs/deploy-hooks)

  * Triggering a deploy
    * Response format
  * Deploying a specific Git commit
  * Deploying from an image registry
  * Using with GitHub Actions
    * 1\. Create a repository secret
    * 2\. Add a GitHub workflow