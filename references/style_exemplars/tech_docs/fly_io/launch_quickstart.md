# Launch Quickstart

**Source**: [https://docs.fly.io/getting-started/launch.md](https://docs.fly.io/getting-started/launch.md)  
**Style Profile**: Direct developer CLI onboarding, no ceremony, transparent infrastructure

---

> ## Documentation Index
> Fetch the complete documentation index at: https://docs.fly.io/llms.txt
> Use this file to discover all available pages before exploring further.

# Quickstart: Launch your app

Welcome to Fly Launch. Fly Launch works with a Dockerfile or scans and configures apps for most [common languages and frameworks](/getting-started/get-started-by-framework).

To deploy your app on Fly.io for the first time:

<Card type="note" className="hide_icon_card">
  1. [Install flyctl](/flyctl/install) – the [open-source](https://github.com/superfly/flyctl) Fly.io CLI.

  2. Create an account with `fly auth signup` or log in with `fly auth login`.

  3. Run `fly launch` from inside your project source directory to create, configure, and (for most apps) deploy a new application.

  4. If prompted, run `fly deploy` to deploy your new app (or to redeploy after changes!).
</Card>

<img src="https://mintcdn.com/fly-io/izaS1l2UMuz6sm1H/images/moto-jump.png?fit=max&auto=format&n=izaS1l2UMuz6sm1H&q=85&s=a7cea651006d8faa34e85012f85d767a" alt="Illustration by Annie Ruygt of a phoenix jumping with a motor bike" width="1299" height="1080" data-path="images/moto-jump.png" />

## Next steps

1. Run `fly status` to show the status of your app and Machines.
2. Run `fly apps open` to open your app in your browser.
3. Learn some [Fly.io essentials](/getting-started/essentials) and continue to [explore what you can do with Fly Launch](/launch/index).

## Grow and scale

Check out some of the ways you can increase availability, capacity, and performance with Fly.io:

* Follow the blueprint for [extra Machines for more resilient apps](/blueprints/resilient-apps-multiple-machines)
* Read up on [App availability and resiliency](/apps/app-availability)
* [Autoscale Machines based on load or custom metrics](/reference/autoscaling)
* [Scale Machine CPU and RAM](/launch/scale-machine)
* [Scale Machine count](/launch/scale-count)

If you have questions, need help, or want to talk about what you're building, visit our [community forum](https://community.fly.io).
