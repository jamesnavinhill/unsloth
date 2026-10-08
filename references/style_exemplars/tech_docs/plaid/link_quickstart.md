# Link - Overview | Plaid Docs

**Source**: [https://plaid.com/docs/link/](https://plaid.com/docs/link/)  
**Style Profile**: Developer-first onboarding, clean step sequences, explicit parameter docs

---

# Link overview

#### Use Link to connect to your users' financial accounts with the Plaid API

#### [Introduction to Link](/docs/link/#introduction-to-link)

Plaid Link is the client-side component that your users will interact with in order to link their accounts to Plaid and allow you to access their accounts via the Plaid API. Using Link is mandatory for all Plaid integrations, except for ones using only the handful of products that do not require end user interaction, such as [Enrich](/docs/enrich/) or the [Identity Verification backend-only flow](/docs/identity-verification/#data-source-checks-without-ui-backend-flow).

__

__

An example Link flow. Your exact flow may differ.

Plaid Link handles all aspects of the login and authentication experience, including credential validation, multi-factor authentication, error handling, and sending account linking confirmation emails. For institutions that use OAuth, Link also manages the OAuth handoff flow, bringing the user to their institution to log in, and then returning them to the Plaid Link experience within your app.

To try Link, see [Plaid Link Demo](https://plaid.com/link-demo/). 

Link is the only available method for connecting accounts and authenticating users in Production. In the Sandbox test environment, Link can optionally be bypassed for testing purposes via [`/sandbox/public_token/create`](/docs/api/sandbox/#sandboxpublic_tokencreate).

#### [Link supported platforms and presentation modes](/docs/link/#link-supported-platforms-and-presentation-modes)For...| Use...  
---|---  
Best mobile UX| Native [iOS](/docs/link/ios/), [Android](/docs/link/android/), [React Native](/docs/link/react-native/), or [Flutter](/docs/link/flutter/) SDKs  
Best web UX| [Native web SDK](/docs/link/web/) (also available with React wrapper)  
Webviews, iFrames, no frontend, or embedded flows where you don't control the frontend| [Hosted Link](/docs/link/hosted-link/)  
  
There are also two optional Link presentation modes you can enable.

For...| Use...  
---|---  
Driving the most end users to choose Plaid| [Embedded Institution Search](/docs/link/embedded-institution-search/)  
Linking multiple banks in a single session (e.g. for PFM use cases)| [Multi-Item Link](/docs/link/multi-item-link/)  
#### [Customizing and optimizing Link](/docs/link/#customizing-and-optimizing-link)

You can customize parts of Link's flow straight from the [Dashboard](https://dashboard.plaid.com/link). You can preview your changes in real time and then publish them instantly once you're ready to go live. For more details, see [Link customization](/docs/link/customization/).

To help you take advantage of the options available for customizing and configuring Link, Plaid offers a [Link best practices guide](/docs/link/best-practices/) and an [in-app messaging guide](/docs/link/messaging/) for advice on how to present Link within your app.

#### [Initializing Link](/docs/link/#initializing-link)

Link is initialized by passing the `link_token` to Link. The exact implementation details for passing the `link_token` will vary by platform. For detailed instructions, see the page for your specific platform: [web](/docs/link/web/), [iOS](/docs/link/ios/), [Android](/docs/link/android/), [React Native](/docs/link/react-native/), [Flutter](/docs/link/flutter/), [mobile webview](/docs/link/webview/), or [Hosted Link](/docs/link/hosted-link/).

For recommendations on configuring the `link_token` for your use case, see [Choosing how to initialize products](/docs/link/initializing-products/).

#### [Link flow overview](/docs/link/#link-flow-overview)

Most Plaid products use Link to generate `public_tokens`. The diagram below shows a model of how Link is used to obtain a `public_token`, which can then be exchanged for an `access_token`, which is used to authenticate requests to the Plaid API. 

Note that some products (including Plaid Check, Identity Verification, Monitor, Document Income, and Payroll Income) do not use a `public_token` or `access_token`. For those products, you will call product endpoints once the end user has completed Link; see product-specific documentation for details on the flow. 

**The Plaid flow** begins when your user wants to connect their bank account to your app.

**1** Call [`/link/token/create`](/docs/api/link/#linktokencreate) to create a `link_token` and pass the temporary token to your app's client.

**2** Use the `link_token` to open Link for your user. In the [`onSuccess` callback](/docs/link/web/#onsuccess), Link will provide a temporary `public_token`. This token can also be obtained on the backend via `/link/token/get`.

**3** Call [`/item/public_token/exchange`](/docs/api/items/#itempublic_tokenexchange) to exchange the `public_token` for a permanent `access_token` and `item_id` for the new `Item`.

**4** Store the `access_token` and use it to make product requests for your user's `Item`.

In code, this flow is initiated by creating a `link_token` and using it to initialize Link. The `link_token` can be configured with the Plaid products you will be using and the countries you will need to support. 

Once the user has logged in via Link, Link will issue a `public_token`. You can obtain the `public_token` through either the frontend or the backend:

  * On the frontend: From the client-side `onSuccess` callback returned by Link after a successful session. For more details on this method, see the Link frontend documentation for your specific platform. 
  * On the backend: From the [`/link/token/get`](/docs/api/link/#linktokenget) endpoint or opt-in [`SESSION_FINISHED`](/docs/api/link/#session_finished) webhook after the Link session has been completed successfully. For more details on this method, see the [Hosted Link](/docs/link/hosted-link/) documentation.

The `public_token` can then be exchanged for an `access_token` via [`/item/public_token/exchange`](/docs/api/items/#itempublic_tokenexchange). 

#### [Error-handling flows](/docs/link/#error-handling-flows)

If your application will access an Item on a recurring basis, rather than just once, it should support [update mode](/docs/link/update-mode/). Update mode allows you to refresh an Item if it enters an error state, such as when a user changes their password or MFA information. For more information, see [Updating an Item](/docs/link/update-mode/).

It's also recommended to have special handling for when a user attempts to link the same Item twice. Requesting access tokens for duplicate Items can lead to higher bills and end-user confusion. To learn more, see [preventing duplicate Items](/docs/link/duplicate-items/).

Occasionally, Link itself can enter an error state if the user takes too long to complete the Link process; a `link_token` expires after 4 hours, or after 30 minutes if it was created for an existing Item in update mode. For information on handling this flow, see [Handling invalid Link tokens](/docs/link/handle-invalid-link-token/).

#### [Supporting OAuth](/docs/link/#supporting-oauth)

Many institutions use an OAuth authentication flow, in which Plaid Link redirects the end user to their bank's website or mobile app to authenticate. To learn more, see the [OAuth guide](/docs/link/oauth/).

#### [Returning user flows](/docs/link/#returning-user-flows)

The returning user flow allows you to enable a faster Plaid Link experience for your users who already use Plaid. To learn more, see [Returning user experience](/docs/link/returning-user/).

#### [Troubleshooting](/docs/link/#troubleshooting)

Since all your users will go through Link, it's important to build as robust an integration as possible. For details on dealing with common problems, see the [Troubleshooting](/docs/link/troubleshooting/) section.

#### [Link updates](/docs/link/#link-updates)

Plaid periodically updates Link to add new functionality and improve conversion. These changes will be automatically deployed. Any test suites and business logic in your app should be robust to the possibility of changes to the user-facing Link flow.

Users of Plaid's SDKs for React, React Native, Flutter, iOS, and Android should regularly update to ensure support for the latest client platforms and Plaid functionality.