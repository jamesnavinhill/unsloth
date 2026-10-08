# Changelog | Stripe Documentation

**Source**: [https://docs.stripe.com/changelog](https://docs.stripe.com/changelog)  
**Style Profile**: Breaking change clarity, deterministic dates, version deprecation explanations

---

# Changelog

## Keep track of changes and upgrades to the Stripe API.

Ask about this page

Copy for LLM

View as Markdown

Install tools

Breaking changesProduct

Category
    All

Relevant changes only

[Sign in](https://dashboard.stripe.com/login?redirect=https%3A%2F%2Fdocs.stripe.com%2Fchangelog) to see changes related to APIs your account uses.

Generally available

Public preview

## Endive

[Learn what's changing in Endive](/changelog/endive)

### 2026-09-30.endive

Breaking changes

#### Payments

[Removes the payment method types parameter from Checkout SessionsCheckout](/changelog/endive/2026-09-30/remove-payment-method-types-checkout-sessions)[Adds support for Data Share Only for 3D Secure authenticationPayments](/changelog/endive/2026-09-30/data-share-only)[Makes Payment Evaluation signal scores nullableRadar](/changelog/endive/2026-09-30/payment-evaluations-nullable-score)[Removes PayTo-specific fields from Payment MethodsPayments](/changelog/endive/2026-09-30/removed-payto-fields)[Enforces collection of billing address parameters for non-EEA SEPA Direct Debit paymentsPayments](/changelog/endive/2026-09-30/require-sepa-direct-debit-address-fields)[Removes the payment method types parameter from Payment Intents and Setup IntentsPayments](/changelog/endive/2026-09-30/removes-the-payment-method-types-parameter-from-payment-intents-and-setup-intents)[Returns specific decline codes for BLIK payment failuresPayments](/changelog/endive/2026-09-30/blik-granular-decline-codes)[Deprecates the payment request buttonElements](/changelog/endive/2026-09-30/deprecate-payment-request-button)[Shows pending-authorization UI for MB WAY, Bizum, and BLIK with stripe.handleNextActionElements](/changelog/endive/2026-09-30/handle-next-action-mb-way-bizum-ui)[Removes support for the payment method types option in ElementsElements](/changelog/endive/2026-09-30/remove-elements-deferred-intent-payment-method-types)[Saves Bancontact payment details for future off-session payments in CheckoutCheckout\+ 2 more](/changelog/endive/2026-09-30/bancontact-off-session-payments-checkout)[Adds the Standalone 3D Secure APIPayments](/changelog/endive/2026-09-30/standalone-3ds)[Adds support for SeQura paymentsPayments](/changelog/endive/2026-09-30/sequra-payments)[Adds card-present payment methods to allowed payment method typesPayments](/changelog/endive/2026-09-30/card-present-and-interac-present-enum-values-for-allowed-payment-method-types)[Adds Link funding source group details on Payment RecordsPayments](/changelog/endive/2026-09-30/link-funding-source-group-payment-records)[Adds early fraud warnings and fraudulent dispute signals for Payment EvaluationsRadar](/changelog/endive/2026-09-30/new-radar-signals-for-payment-evaluations)[Adds the ability to report canceled paymentsPayments](/changelog/endive/2026-09-30/reporting-canceled-payments)[Adds support for expanding the mandate on card payment method detailsPayments](/changelog/endive/2026-09-30/expand-mandate-on-card-payments-details)[Adds the Payment Record property to the Payment Intent objectPayments](/changelog/endive/2026-09-30/payment-records-on-payment-intents)[Adds Link wallet details to Payment Records for card paymentsPayments](/changelog/endive/2026-09-30/adds-link-wallet-details-to-payment-records-for-card-payments)[Adds 3D Secure versions 2.3.0 and 2.3.1 to Payment RecordsPayments](/changelog/endive/2026-09-30/3d-secure-payment-records)[Adds support for BLIK recurring off-session paymentsPayments\+ 3 more](/changelog/endive/2026-09-30/blik-recurring-off-session-payments)[Adds PayPay support for one-time online payments in JapanPayments](/changelog/endive/2026-09-30/paypay-payments-japan)[Exposes the network response electronic commerce indicator on card chargesPayments](/changelog/endive/2026-09-30/view-network-response-eci-on-card-charges)[Adds payment method type information for failed paymentsPayments](/changelog/endive/2026-09-30/payment-method-type-payment-failures)[Adds MoMo payment method details to Payment RecordsPayments](/changelog/endive/2026-09-30/adds-momo-payment-method-details-to-payment-records)

#### Connect and accounts

[Adds address validation errors for CMRAs and registered agents to Accounts v1 and Accounts v2Issuing\+ 1 more](/changelog/endive/2026-09-30/address-validation-cmra-registered-agents-accounts-v2)[Adds rejected status for Accounts v2 capabilitiesConnect](/changelog/endive/2026-09-30/rejected-accounts-v2-capabilities)[Replaces the generic fraud rejection reason with specific fraud reasonsConnect](/changelog/endive/2026-09-30/updated-reject-reason-codes)[Removes the configurations parameter from the Account Links v2 APIAffects all products](/changelog/endive/2026-09-30/removes-configurations-parameter-from-v2-core-account-links-api)[Standardizes SEPA Direct Debit payment settings in the Accounts APIConnect\+ 1 more](/changelog/endive/2026-09-30/sepa-debit-settings-accounts)[Shows errors for eventually due requirementsConnect](/changelog/endive/2026-09-30/shows-errors-for-eventually-due-requirements)[Distinguishes platform-initiated account rejections from Stripe rejectionsConnect](/changelog/endive/2026-09-30/platform-rejection-reasons)[Adds additional shared fields to customer sharingAffects all products](/changelog/endive/2026-09-30/additional-shared-fields-customer-sharing)

#### Billing and invoicing

[Unifies the billing cycle anchor format across Subscriptions and InvoicesBilling](/changelog/endive/2026-09-30/polymorphic-billing-cycle-anchor)[Adds invoicing rules to Invoice ItemsBilling](/changelog/endive/2026-09-30/invoicing-rules-for-invoice-items)[Adds reference and company details parameters for BilliePayments\+ 2 more](/changelog/endive/2026-09-30/reference-and-company-details-billie)[Adds the ability to clear invoicing rules on Invoice ItemsBilling](/changelog/endive/2026-09-30/clear-invoicing-rules-on-invoice-items)[Adds proration details for Invoice Items using classic billing modeBilling](/changelog/endive/2026-09-30/invoice-items-proration-details)[Makes trial offers generally availableBilling](/changelog/endive/2026-09-30/trial-offer-ga)[Adds detailed status to explain why an Invoice is uncollectableBilling](/changelog/endive/2026-09-30/invoice-uncollectible-status-detail)[Adds support for scheduling Subscription cancellation as part of pending updateBilling](/changelog/endive/2026-09-30/scheduled-subscription-cancellation)[Adds the ability to pause and resume Subscriptions on demandBilling](/changelog/endive/2026-09-30/pause-subscription)[Adds the Feedback Options APIBilling](/changelog/endive/2026-09-30/feedback-options-api)

#### Tax

[Adds Failed Tax Calculation errorTax\+ 3 more](/changelog/endive/2026-09-30/failed-tax-calculation-error)[Adds support for new tax typesTax](/changelog/endive/2026-09-30/stripe-tax-new-tax-types)[Adds support for ticket sales to Stripe TaxBilling\+ 3 more](/changelog/endive/2026-09-30/stripe-tax-tickets)

#### Financial Connections

[Renames the countries filter to country on Financial Connections SessionsFinancial Connections](/changelog/endive/2026-09-30/rename-financial-connections-countries-filter-to-country)[Updates Financial Connections Session defaultsFinancial Connections](/changelog/endive/2026-09-30/financial-connections-session-defaults)[Adds pending and expired statuses to Financial Connections account numbersFinancial Connections](/changelog/endive/2026-09-30/pending-and-expired-status-added-to-financial-connections-account-numbers)

#### Treasury and money management

[Renames the Reserve Release reason enum valueRadar](/changelog/endive/2026-09-30/reserve-release-reason)[Adds destination property and new enum values to Reserve Plans, Holds and ReleasesTreasury\+ 1 more](/changelog/endive/2026-09-30/settlement-reserve-api)[Adds support for received credits sent via the Real-Time Payments networkTreasury](/changelog/endive/2026-09-30/rtp-network-received-credits)[Exposes ACH return codes on OutboundPayments, OutboundTransfers, and InboundTransfers in v1 TreasuryTreasury](/changelog/endive/2026-09-30/v1-treasury-ach-return-codes)

#### Additional updates

[Adds page limit validation for dispute evidencePayments](/changelog/endive/2026-09-30/page-limit-validation-dispute-evidence)[Rejects duplicate references for pending India card mandatesPayments](/changelog/endive/2026-09-30/duplicate-reference-validation-for-india-pending-mandates)[Surfaces India card mandates on Charges and SetupIntents even when inactivePayments](/changelog/endive/2026-09-30/surface-india-card-mandate-even-when-inactive)[Sets canConfirm to false while updates are pending in Elements with Checkout SessionsCheckout\+ 1 more](/changelog/endive/2026-09-30/block-custom-checkout-confirmation-pending-updates)[Allows empty optional address fields in Elements with Checkout SessionsCheckout\+ 1 more](/changelog/endive/2026-09-30/skip-format-validation-empty-optional-address-fields)[Requires billing details when Payment Element collection is disabledCheckout\+ 1 more](/changelog/endive/2026-09-30/strict-billing-details-validation)[Makes thin events for API v1 resources generally availableAffects all products](/changelog/endive/2026-09-30/thin-events-for-api-v1-resources-generally-available)[Adds Satispay payments capability to Accounts v2Affects all products](/changelog/endive/2026-09-30/satispay-payments-capability-for-accounts-v2-api)[Adds an expiration timestamp to the Swish QR code objectTerminal](/changelog/endive/2026-09-30/expiration-timestamp-swish-qr)[Adds a new outcome type for rerouted payments to Payment EvaluationsRadar](/changelog/endive/2026-09-30/adds-a-new-outcome-type-for-rerouted-bank-payments-to-payment-evaluations)[Adds Balance Transaction types for provisional credits for Issuing disputesIssuing](/changelog/endive/2026-09-30/provisional-credit-issuing-disputes-balance-transaction-types)[Adds India-specific mandate details to card payment method responsesPayments](/changelog/endive/2026-09-30/india-specific-mandate-card-payments)[Adds the option to automatically pause subscriptions after payment failuresBilling](/changelog/endive/2026-09-30/pause-on-payment-failure)[Adds the Install API for Stripe AppsAffects all products](/changelog/endive/2026-09-30/install-api)

## 2024

[2024-06-20](/changelog/2024-06-20)

Breaking changes

[Renames a `fuel` attribute of the `Authorization` objectIssuing](/changelog/2024-06-20/renames-fuel-attribute-authorization-object)[Renames a `purchase_details` attribute of the `Transaction` objectIssuing](/changelog/2024-06-20/renames-purchase-details-transaction-object)[Removes undocumented fuel fieldsIssuing](/changelog/2024-06-20/removes-undocumented-fuel-fields-issuing)[Removes undocumented fleet fieldsIssuing](/changelog/2024-06-20/removes-undocumented-fleet-fields-issuing)[Adds enum values for fuel unitsIssuing](/changelog/2024-06-20/adds-enum-fuel-units-issuing)[Deprecates `alphanumeric_id` for Issuing AuthorizationIssuing](/changelog/2024-06-20/deprecates-alphanumeric-id-issuing)[Adds enum values for disabled reasonsConnect](/changelog/2024-06-20/adds-enum-disabled-reasons-capabilities)[Deprecates the `bank_transfer_payments` capability type in favor of newer capability typesConnect](/changelog/2024-06-20/deprecates-bank-transfer-payments-capabilities)[Adds new enum values for request history reasonsIssuing](/changelog/2024-06-20/adds-enum-request-history-reasons-issuing)

[2024-04-10](/changelog/2024-04-10)

Breaking changes

[Makes automatic async the default capture method for PaymentIntents when not specifiedPayments](/changelog/2024-04-10/automatic-sync-default-paymentintents)[Renames the `rendering_options` attribute for invoices to `rendering`Invoicing\+ 1 more](/changelog/2024-04-10/renames-rendering-options-invoicing)[Renames the `features` attribute of the `Product` objectInvoicing\+ 1 more](/changelog/2024-04-10/renames-features-attribute-product-object)

## 2023

[2023-10-16](/changelog/2023-10-16)

Breaking changes

[Adds new account requirement error codes to the Accounts APIConnect](/changelog/2023-10-16/adds-account-requirement-error-accounts)[Auto-populates the statement descriptor and prefix in the Accounts APIConnect](/changelog/2023-10-16/auto-populates-statement-descriptor-accounts)

[2023-08-16](/changelog/2023-08-16)

Breaking changes

[Enables automatic payment methods by default for PaymentIntents and SetupIntentsPayments\+ 1 more](/changelog/2023-08-16/automatic-payment-methods)[One-time payments in Checkout Sessions support no-cost ordersCheckout](/changelog/2023-08-16/no-cost-orders-checkout-session)[Platform-scope rendering for select PaymentMethod fingerprintsConnect\+ 2 more](/changelog/2023-08-16/platform-scope-rendering-payment-method)[Adds specific error codes for failed Klarna paymentsPayments\+ 1 more](/changelog/2023-08-16/klarna-payment-failure-error-code)[Adds new director verification error codes to the Accounts APIConnect](/changelog/2023-08-16/adds-director-verfication-error-accounts)

## 2022

[2022-11-15](/changelog/2022-11-15)

Breaking changes

[The `Charges` object no longer auto-expands refunds by defaultPayments](/changelog/2022-11-15/deprecates-charges-auto-expand)[Removes the `charges` attribute from the `PaymentIntent` objectPayments](/changelog/2022-11-15/removes-charges-attribute-paymentintent)[Adds new decline codes to the PaymentIntent and PaymentMethod APIsPayments](/changelog/2022-11-15/adds-decline-codes-paymentintent-paymentmethod)[Adds new decline codes to the SetupIntent APIPayments](/changelog/2022-11-15/adds-decline-codes-setupintent)[Adds a new structure error code to the Accounts APIConnect](/changelog/2022-11-15/adds-structure-error-code-accounts)

[2022-08-01](/changelog/2022-08-01)

Breaking changes

[Removes the `include_and_require` value when creating invoicesInvoicing](/changelog/2022-08-01/removes-include-require-value-invoices)[Default customer creation in Checkout Session payment mode changed to `if_required`Checkout](/changelog/2022-08-01/default-customer-creation-checkout-session)[Deferred PaymentIntent creation in Checkout Session payment modeCheckout\+ 1 more](/changelog/2022-08-01/deferred-paymentintent-checkout-session)[Removes the `setup_intent` property from Checkout Sessions in subscription modeCheckout](/changelog/2022-08-01/removes-setupintent-checkout-session)[Replaces line item parameters from the Create Checkout Session endpointCheckout](/changelog/2022-08-01/replaces-line-item-create-checkout-session)[Removes the subscription data parameter from the Create Checkout Session endpointCheckout\+ 1 more](/changelog/2022-08-01/removes-subscription-data-create-checkout-session)[Removes the shipping rate parameter from Create Checkout Session endpointCheckout](/changelog/2022-08-01/removes-shipping-rate-create-checkout-session)[Updates Checkout Session shipping propertiesCheckout](/changelog/2022-08-01/updates-shipping-property-checkout-session)[Adds 3D Secure exemption status to card chargesPayments](/changelog/2022-08-01/adds-3d-secure-exemption-charges)[New error code for invalid terms of service acceptance in Accounts APIConnect](/changelog/2022-08-01/error-code-invalid-tos-accounts)[New endpoints for managing a physical card’s shipping status in test modeIssuing](/changelog/2022-08-01/endpoints-shipping-status-cards)[Adds `design_rejected` as a possible cancellation reason for issued cardsIssuing](/changelog/2022-08-01/adds-design-rejected-value-cards)[Removes the `default_currency` attribute from the `Customer` objectAffects all products](/changelog/2022-08-01/removes-default-currency-customer-object)

## 2020

[2020-08-27](/changelog/2020-08-27)

Breaking changes

[Removes the `tax_percent` attributeCheckout\+ 2 more](/changelog/2020-08-27/removes-tax-percent-attribute)[Renames `phases` attributes in subscription schedulesBilling](/changelog/2020-08-27/renames-phases-attributes-subscription-schedules)[Renames event type that triggers on automatic updatesPayments](/changelog/2020-08-27/renames-automatically-updated-event-type)[Removes the `display_items` property from Checkout SessionsCheckout](/changelog/2020-08-27/removes-display-items-checkout-session)[Formats requirements for key persons associated with accountsConnect](/changelog/2020-08-27/formats-requirements-key-persons-accounts)[Adds new error codes to the Accounts, Persons, and Capabilities APIsConnect](/changelog/2020-08-27/adds-error-codes-accounts-persons-capabilities)[Updates to 3D Secure details in `Charge` objectPayments](/changelog/2020-08-27/updates-3d-scure-charge-object)[Customer subscriptions are no longer auto-expanded by defaultBilling](/changelog/2020-08-27/deprecates-auto-expansion-customer-subscriptions)[Plan tiers are no longer auto-expanded by defaultBilling](/changelog/2020-08-27/deprecates-auto-expansion-plan-tiers)[Customer sources are no longer auto-expanded by defaultPayments\+ 2 more](/changelog/2020-08-27/deprecates-auto-expansion-customer-sources)[Tax IDs are no longer auto-expanded on the `Customer` objectAffects all products](/changelog/2020-08-27/deprecates-auto-expansion-tax-id-customer)[Deprecates subscription `prorate` and `subscription_prorate` parametersBilling](/changelog/2020-08-27/deprecates-prorate-parameters-subscriptions)

[2020-03-02](/changelog/2020-03-02)

Breaking changes

[Invoices can now be numbered sequentially across your accountBilling\+ 1 more](/changelog/2020-03-02/sequentially-number-invoices)

## 2019

[2019-12-03](/changelog/2019-12-03)

Breaking changes

[Standardizes invoice line item IDsBilling\+ 1 more](/changelog/2019-12-03/standardizes-invoice-line-item-ids)[New requirement for `out_of_band_amount` when creating post-payment credit notesBilling\+ 1 more](/changelog/2019-12-03/post-payment-credit-note-requirement)[Customer balances are now returned when voiding invoicesBilling\+ 1 more](/changelog/2019-12-03/customer-balances-returned-voided-invoices)[Removes deprecated tax information fields from the `Customer` objectAffects all products](/changelog/2019-12-03/removes-deprecated-tax-information-fields)

[2019-11-05](/changelog/2019-11-05)

Breaking changes

[Adds requirement for `requested_capabilities` on custom account creationConnect](/changelog/2019-11-05/adds-requested-capabilities-requirement-custom-account)[Nested subscription schedule settings under `default_settings`Billing](/changelog/2019-11-05/nests-subscription-schedule-settings)

[2019-10-17](/changelog/2019-10-17)

Breaking changes

[Renames and updates subscription schedule renewal propertiesBilling](/changelog/2019-10-17/updates-subscription-renewal-properties)[Replaces the subscription `start` field with `start_date`Billing](/changelog/2019-10-17/replaces-subscription-start-field)[Renames `billing` to `collection_method` on invoices, subscriptions, and subscription schedulesBilling\+ 1 more](/changelog/2019-10-17/renames-billing-attribute)[The `due_date` property is always null on auto-billed invoicesBilling\+ 1 more](/changelog/2019-10-17/invoice-due-date-null)[Renames `account_balance` to `balance` on `Customer` objectBilling\+ 1 more](/changelog/2019-10-17/renames-account-balance-customer-object)

[2019-10-08](/changelog/2019-10-08)

Breaking changes

[Renames a `Person` object relationship attributeConnect](/changelog/2019-10-08/renames-person-object-relationship-attribute)

[2019-09-09](/changelog/2019-09-09)

Breaking changes

[Accounts in many countries now require specifying capabilities at creation timeConnect](/changelog/2019-09-09/2019-09-09-1)[Adds new `details_code` values to person document verificationConnect](/changelog/2019-09-09/adds-detail-code-person-document-verification)

[2019-08-14](/changelog/2019-08-14)

Breaking changes

[Renames the `platform_payments` capability for accounts to `card_payments`, requiring the manual specification of the added `transfers` capabilityConnect](/changelog/2019-08-14/configuring-person-account-opener-no-longer-sets-executive)[Configuring a person as an account opener no longer automatically sets them as an executiveConnect](/changelog/2019-08-14/accounts-many-countries-require-specifying-capabilities)

[2019-05-16](/changelog/2019-05-16)

Breaking changes

[Bank pull payments no longer expose internal system refunds on failurePayments](/changelog/2019-05-16/renames-platform-payments-capability-card-payments)

[2019-03-14](/changelog/2019-03-14)

Breaking changes

[Renames `application_fee` on invoices to `application_fee_amount`Connect\+ 1 more](/changelog/2019-03-14/renames-application-fee-invoices-application-fee-amount)[Subscriptions are now successfully created even if the first payment failsBilling](/changelog/2019-03-14/subscriptions-successfully-created-first-payment-fails)[Invoices now provide timestamps for each state transitionBilling\+ 1 more](/changelog/2019-03-14/invoices-provide-timestamps-state-transitions)[Renames the `date` field for invoices to `created`Billing\+ 1 more](/changelog/2019-03-14/renames-date-field-invoices-created)[Invoices now specify when they’re finalized alongside other status transitionsBilling\+ 1 more](/changelog/2019-03-14/invoices-specify-finalized-alongside-status-transitions)

[2019-02-19](/changelog/2019-02-19)

Breaking changes

[Changes statement descriptor behaviors for card payments created with ChargesPayments](/changelog/2019-02-19/changes-statement-descriptor-behaviors-charges)[Several account fields have been refactored to better describe legal entity, verification status and requirements, and configurable settingsConnect](/changelog/2019-02-19/several-fields-accounts-refactored)[Several fields describing an account’s business details have moved to the `business_profile` subhashConnect](/changelog/2019-02-19/business-details-moved-business-profile-object)[Verification of accounts or persons now supports uploading both front and back sidesConnect](/changelog/2019-02-19/verification-accounts-persons-supports-front-back)[Accounts no longer provide a `keys` field. Platforms should use their own API key to authenticate as their connected accountsConnect](/changelog/2019-02-19/accounts-no-longer-provide-keys-field)[Accounts in the US now require specifying capabilities at creation timeConnect](/changelog/2019-02-19/accounts-us-require-specifying-capabilities-creation)[Renames the `business_id_number` for an account’s legal entity to `business_registration_number`Connect](/changelog/2019-02-19/renames-business-id-number-business-registration-number)

[2019-02-11](/changelog/2019-02-11)

Breaking changes

[Renames several statuses for PaymentIntentsPayments](/changelog/2019-02-11/renames-several-statuses-payment-intents)[Renames the `save_source_to_customer` field for sources to `save_payment_method`Payments](/changelog/2019-02-11/renames-save-source-to-customer-save-payment-method)[Renames the `allowed_source_types` field for `sources` to `payment_method_types`Payments](/changelog/2019-02-11/renames-allowed-source-types-payment-method-types)[Renames the `next_source_action` field for Payment Intents to `next_action`Payments](/changelog/2019-02-11/renames-next-source-action-next-action)[Renames the `authorize_with_url` field for Payment Intents to `redirect_to_url`Payments](/changelog/2019-02-11/renames-authorize-with-url-redirect-to-url)

## 2018

[2018-11-08](/changelog/2018-11-08)

Breaking changes

[Invoices now specify their automatic collection behavior using the `auto_advance` fieldInvoicing\+ 1 more](/changelog/2018-11-08/invoices-specify-auto-advance-field)[One-off Invoices no longer automatically collect payment by defaultInvoicing](/changelog/2018-11-08/one-off-invoices-no-longer-auto-collect-payment)[Replaces the `forgiven` field with a new `uncollectible` status for invoicesInvoicing\+ 1 more](/changelog/2018-11-08/mark-invoice-uncollectible-instead-forgiven)[Renames an invoice error code to `invoice_already_finalized`Invoicing\+ 1 more](/changelog/2018-11-08/renames-invoice-error-code-invoice-already-finalized)[Includes several changes for users of the Payment Intents API private betaPayments](/changelog/2018-11-08/several-changes-payment-intents-private-beta)

[2018-10-31](/changelog/2018-10-31)

Breaking changes

[Descriptions for customers now have a character limitAffects all products](/changelog/2018-10-31/descriptions-customers-character-limit)[Product names now have a character limitBilling\+ 1 more](/changelog/2018-10-31/names-products-character-limit)[Descriptions for invoice line items now have a character limitBilling\+ 1 more](/changelog/2018-10-31/descriptions-invoice-line-items-character-limit)[The `billing_reason` of the first invoice of a subscription is now `subscription_create`Billing\+ 1 more](/changelog/2018-10-31/first-invoice-subscription-billing-reason-subscription-create)

[2018-09-24](/changelog/2018-09-24)

Breaking changes

[Renames the `FileUpload` object to `Files`, which now require secret keys to download filesAffects all products](/changelog/2018-09-24/file-uploads-renamed-files-require-secret-keys)

[2018-09-06](/changelog/2018-09-06)

Breaking changes

[SKU values no longer need to be uniqueCheckout](/changelog/2018-09-06/sku-values-no-longer-need-unique)

[2018-08-23](/changelog/2018-08-23)

Breaking changes

[A subscription’s ending period can no longer be configured while canceling itBilling](/changelog/2018-08-23/subscription-ending-period-cannot-configured-canceling)[Customers now provide a `tax_info` object with their tax ID detailsAffects all products](/changelog/2018-08-23/customers-provide-tax-info-object)[Renames the `amount` field for plan tiers to `unit_amount`Billing](/changelog/2018-08-23/renames-amount-field-plan-tiers-unit-amount)

[2018-07-27](/changelog/2018-07-27)

Breaking changes

[Subscriptions no longer support modifying the `source` parameter directlyBilling](/changelog/2018-07-27/subscriptions-no-longer-support-modifying-source)[Ending a subscription trial now uses the timestamp of that API requestBilling](/changelog/2018-07-27/ending-subscription-trial-uses-request-timestamp)[Coupons now use floats rather than integers to specify `percent_off`Billing\+ 1 more](/changelog/2018-07-27/coupons-use-floats-specify-percent-off)[Stripe now validates email addresses when creating or updating customersAffects all products](/changelog/2018-07-27/stripe-validates-email-addresses-customers)

[2018-05-21](/changelog/2018-05-21)

Breaking changes

[Products no longer embed lists of SKUsCheckout](/changelog/2018-05-21/products-no-longer-embed-sku-lists)[Invoice line items now have unique IDs and can’t be used in place of a subscriptionBilling\+ 1 more](/changelog/2018-05-21/invoice-line-items-have-unique-ids-cannot-use-subscription)[Coupons, SKUs, customers, products, and plans now limit the valid characters for IDsBilling\+ 1 more](/changelog/2018-05-21/valid-characters-ids-coupons-skus-customers-products-plans)[Subscriptions now default to not defining their trial periods depending on a planBilling](/changelog/2018-05-21/subscriptions-default-no-trial-period-plan)[Changing a subscription to a new plan with a trial now extends the trial periodBilling](/changelog/2018-05-21/changing-subscription-new-plan-extends-trial)

[2018-02-28](/changelog/2018-02-28)

Breaking changes

[Updating a canceled subscription on a future date no longer resets its statusBilling](/changelog/2018-02-28/updating-canceled-subscription-no-longer-resets-status)

[2018-02-06](/changelog/2018-02-06)

Breaking changes

[Sources now provide a `recommended` value when the issuer advises using 3D SecurePayments](/changelog/2018-02-06/sources-provide-recommended-use-3d-secure)

[2018-02-05](/changelog/2018-02-05)

Breaking changes

[Free plans with prorations now produce zero-dollar invoicesBilling](/changelog/2018-02-05/free-plans-with-prorations-produce-zero-dollar-invoices)[Subscriptions can now delay the first full invoice to a future date (and optionally include a free trial)Billing](/changelog/2018-02-05/subscriptions-delay-first-full-invoice-future-date)[Plans now link to individual products, with several fields moving to the product resourceBilling](/changelog/2018-02-05/plans-link-individual-products-several-fields-moved)[Products now require a `type` field, differentiating their use with order SKUs or subscriptions and plansBilling\+ 1 more](/changelog/2018-02-05/products-require-type-field-differentiating-use)

[2018-01-23](/changelog/2018-01-23)

Breaking changes

[Connect platforms can identify reused card or bank accounts across connected accounts as they now will share the same fingerprintConnect](/changelog/2018-01-23/connect-platforms-identify-reused-cards-bank-accounts)

## 2017

[2017-12-14](/changelog/2017-12-14)

Breaking changes

[Invoice line items now must always set a `description`Invoicing\+ 1 more](/changelog/2017-12-14/invoice-line-items-must-set-description)[Invoice payment failures now return a `card_error` when a charge is declinedInvoicing\+ 1 more](/changelog/2017-12-14/invoice-payment-failures-return-card-error)

[2017-08-15](/changelog/2017-08-15)

Breaking changes

[Sources can now specify that an authentication redirect isn’t requiredPayments](/changelog/2017-08-15/sources-specify-no-authentication-redirect-required)

[2017-06-05](/changelog/2017-06-05)

Breaking changes

[Accounts can now specify why an account isn’t enabled with the new reason `under_review`Connect](/changelog/2017-06-05/accounts-specify-under-review-reason)

[2017-05-25](/changelog/2017-05-25)

Breaking changes

[Events for Connect now specify the originating connected account using the `account` fieldConnect](/changelog/2017-05-25/events-connect-specify-originating-account)[The `request` field of the `Events` object now specifies both the request ID and idempotency keyAffects all products](/changelog/2017-05-25/events-specify-request-id-idempotency-key)[Events with the `previous_attributes` field now render the complete affected sub-arrayAffects all products](/changelog/2017-05-25/events-previous-attributes-render-complete-sub-array)[Accounts must now specify one of three types (Standard, Express, or Custom)Connect](/changelog/2017-05-25/accounts-specify-type-standard-express-custom)

[2017-04-06](/changelog/2017-04-06)

Breaking changes

[Transfers are now split into payouts and transfersConnect](/changelog/2017-04-06/transfers-split-payouts-transfers)

[2017-02-14](/changelog/2017-02-14)

Breaking changes

[Charges now specify the ID for the rule blocking a transaction, which can be expandedPayments\+ 1 more](/changelog/2017-02-14/charges-specify-rule-blocking-transaction)[Charges now specify the ID for the dispute associated with a transaction, which can be expandedPayments](/changelog/2017-02-14/charges-specify-dispute-associated-transaction)

[2017-01-27](/changelog/2017-01-27)

Breaking changes

[Balance transactions no longer include the `sourced_transfers` fieldPayments\+ 1 more](/changelog/2017-01-27/balance-transactions-no-longer-include-sourced-transfers)

## 2016

[2016-10-19](/changelog/2016-10-19)

Breaking changes

[Using insufficient permissions to make API requests now throws an HTTP 403 errorAffects all products](/changelog/2016-10-19/insufficient-permissions-throw-403-error)

[2016-07-06](/changelog/2016-07-06)

Breaking changes

[Filter lists of subscriptions for canceled subscriptionsBilling](/changelog/2016-07-06/filter-canceled-subscriptions-retrieve-individually)

[2016-06-15](/changelog/2016-06-15)

Breaking changes

[Deactivating a product no longer automatically deactivates its SKUsBilling](/changelog/2016-06-15/deactivating-product-deactivates-skus)

[2016-03-07](/changelog/2016-03-07)

Breaking changes

[Supported currencies are defined on the country spec for an account’s countryPayments](/changelog/2016-03-07/supported-currencies-defined-country-spec)

[2016-02-29](/changelog/2016-02-29)

Breaking changes

[Creating or updating an account now validates the postal code for its legal entityConnect](/changelog/2016-02-29/creating-updating-account-validates-postal-code)

[2016-02-23](/changelog/2016-02-23)

Breaking changes

[Orders that are paid or fulfilled, and then become canceled or returned, now automatically refund associated chargesPayments](/changelog/2016-02-23/orders-paid-fulfilled-refund-associated-charges)

[2016-02-22](/changelog/2016-02-22)

Breaking changes

[You can no longer add more than 250 invoice items to an invoiceBilling\+ 1 more](/changelog/2016-02-22/no-more-than-250-invoice-items)

[2016-02-19](/changelog/2016-02-19)

Breaking changes

[Renames the `name` field on Bank Accounts to `account_holder_name`Payments](/changelog/2016-02-19/renames-name-field-bank-accounts-account-holder-name)

[2016-02-03](/changelog/2016-02-03)

Breaking changes

[Accounts now only show country-specific subfields for the `legal_entity` fieldConnect](/changelog/2016-02-03/accounts-only-show-country-fields-legal-entity)

## 2015

[2015-10-16](/changelog/2015-10-16)

Breaking changes

[Creating or updating customers must now include a plan if a tax percentage is specifiedBilling](/changelog/2015-10-16/customers-must-include-plan-tax-percentage)

[2015-10-12](/changelog/2015-10-12)

Breaking changes

[Using invalid parameters to create cards or bank accounts for tokens, sources, or external bank accounts now throws an HTTP 400 errorPayments](/changelog/2015-10-12/invalid-parameters-throw-400-error)

[2015-10-01](/changelog/2015-10-01)

Breaking changes

[Bank account information renamed to external accounts on user profilesConnect](/changelog/2015-10-01/accounts-include-external-accounts-field)[Accounts now include an `external_accounts` fieldConnect](/changelog/2015-10-01/accounts-specify-additional-fields-bank-accounts)

[2015-09-23](/changelog/2015-09-23)

Breaking changes

[The `charge` field now always reflects the latest charge on invoicesInvoicing\+ 1 more](/changelog/2015-09-23/invoice-charge-field-reflect-latest-charge)[Invoices no longer include the `payment` propertyInvoicing\+ 1 more](/changelog/2015-09-23/invoices-no-longer-include-payment-field)[Listing all charges now includes payments from all funding sourcesPayments](/changelog/2015-09-23/listing-charges-includes-payments-funding-sources)[Charges only support an `offset` for list pagination when filtering by sourcePayments](/changelog/2015-09-23/charges-support-offset-list-pagination-source)

[2015-09-08](/changelog/2015-09-08)

Breaking changes

[Rate-limited requests now return an HTTP 429 error, no longer including the `rate_limit` fieldAffects all products](/changelog/2015-09-08/rate-limited-requests-return-429-no-rate-limit)

[2015-09-03](/changelog/2015-09-03)

Breaking changes

[Requests that reuse idempotency tokens but alter request parameters now throw an errorAffects all products](/changelog/2015-09-03/reuse-idempotency-tokens-alter-error)

[2015-08-19](/changelog/2015-08-19)

Breaking changes

[Balance transactions with refunds or disputes now specify the corresponding ID in the `source` fieldPayments](/changelog/2015-08-19/balance-transactions-refunds-disputes-specify-source)

[2015-08-07](/changelog/2015-08-07)

Breaking changes

[Stripe now ensures the `tos_acceptance[date]` field on accounts is a valid timestampConnect](/changelog/2015-08-07/stripe-ensures-tos-acceptance-date-valid-timestamp)

[2015-07-28](/changelog/2015-07-28)

Breaking changes

[Transfers that are immediately processed now trigger the `balance.available` eventConnect](/changelog/2015-07-28/transfers-immediately-processed-trigger-balance-available)

[2015-07-13](/changelog/2015-07-13)

Breaking changes

[Accounts now include the `verification[disabled_reason]` field to describe why they can’t make transfers or chargesConnect](/changelog/2015-07-13/accounts-include-verification-disabled-reason-field)

[2015-07-07](/changelog/2015-07-07)

Breaking changes

[Transfers submitted to the bank that haven’t arrived now provide an `in_transit` statusConnect](/changelog/2015-07-07/transfers-in-transit-provide-status)

[2015-06-15](/changelog/2015-06-15)

Breaking changes

[Accounts on manual payout schedules now throw a new errorConnect](/changelog/2015-06-15/accounts-manual-payout-schedules-throw-error)

[2015-04-07](/changelog/2015-04-07)

Breaking changes

[Updates how ending periods are calculated on prorated invoice line itemsBilling](/changelog/2015-04-07/updates-ending-periods-prorated-invoice-line-items)[Changes the sorting order of `lines` for invoicesBilling\+ 1 more](/changelog/2015-04-07/changes-sorting-order-lines-invoices)

[2015-03-24](/changelog/2015-03-24)

Breaking changes

[By default, coupons no longer apply to invoice items with negative amountsBilling\+ 1 more](/changelog/2015-03-24/coupons-no-longer-apply-negative-invoice-items)

[2015-02-18](/changelog/2015-02-18)

Breaking changes

[Charges that succeed now have a `succeeded` statusPayments](/changelog/2015-02-18/charges-succeed-have-succeeded-status)[Charges now have a `source` field that accepts a source or cardPayments](/changelog/2015-02-18/charges-have-source-field-accepts-source-card)[Customers now have a `source` field that accepts a source or card, and updates related event typesPayments](/changelog/2015-02-18/customers-have-source-field-accepts-source-card)

[2015-02-16](/changelog/2015-02-16)

Breaking changes

[Renames the `transfer.canceled` event type to `transfer.reversed`Connect](/changelog/2015-02-16/renames-transfer-canceled-event-transfer-reversed)

[2015-02-10](/changelog/2015-02-10)

Breaking changes

[Dispute statuses now include the `warning_closed` valuePayments](/changelog/2015-02-10/dispute-statuses-include-warning-closed)[Transfers now require a sufficient account balance in test mode to better simulate live modeConnect](/changelog/2015-02-10/transfers-require-sufficient-balance-test-mode)

[2015-01-26](/changelog/2015-01-26)

Breaking changes

[Events with the `previous_attributes` field now only render the differences to objects across updatesAffects all products](/changelog/2015-01-26/events-previous-attributes-render-differences)[Subscriptions now only report the timestamp for API or invoice payment failures for the `canceled_at` fieldBilling](/changelog/2015-01-26/subscriptions-report-api-invoice-failures)

[2015-01-11](/changelog/2015-01-11)

Breaking changes

[File uploads describe their file type with the simpler `type` field and formatAffects all products](/changelog/2015-01-11/file-uploads-describe-type-format)

## 2014

[2014-12-22](/changelog/2014-12-22)

Breaking changes

[Cards now use both the `unchecked` and `unavailable` values to describe address and CVC checks by issuing banksPayments](/changelog/2014-12-22/cards-use-unchecked-unavailable-address-cvc-checks)[Tokens with cards no longer include the `customer` fieldPayments](/changelog/2014-12-22/tokens-cards-no-longer-include-customer-field)

[2014-12-17](/changelog/2014-12-17)

Breaking changes

[Introduces the `statement_description` field and logic for how charges, invoices, plans, and transfers render statement descriptorsPayments\+ 3 more](/changelog/2014-12-17/introduces-statement-description-field-logic)[Creating accounts using the API requires the 2014-12-17 version or newerConnect](/changelog/2014-12-17/creating-accounts-requires-2014-12-17-version)

[2014-12-08](/changelog/2014-12-08)

Breaking changes

[Disputes now include an `evidence_details` object for evidence documentationPayments](/changelog/2014-12-08/disputes-include-evidence-details-object)

[2014-11-20](/changelog/2014-11-20)

Breaking changes

[Disputes are now reported as `won` even if the charge is refundedPayments](/changelog/2014-11-20/disputes-reported-won-refunded-charge)[Invoice items now reflect the metadata for their associated subscription, rather than planBilling](/changelog/2014-11-20/invoice-items-reflect-subscription-metadata)

[2014-11-05](/changelog/2014-11-05)

Breaking changes

[Account activation status terms updated for payments and transfersConnect](/changelog/2014-11-05/renames-charge-account-enabled-fields)

[2014-10-07](/changelog/2014-10-07)

Breaking changes

[You can no longer retrieve tokens with publishable keysElements](/changelog/2014-10-07/no-longer-retrieve-tokens-publishable-keys)[Creating a Card or Bank Account with a publishable key omits fingerprints in API responsesElements](/changelog/2014-10-07/create-card-bank-account-omit-fingerprints)

[2014-09-08](/changelog/2014-09-08)

Breaking changes

[Bank Accounts now include a `status` enum that replace multiple fieldsPayments](/changelog/2014-09-08/bank-accounts-include-status-enum)

[2014-08-20](/changelog/2014-08-20)

Breaking changes

[Disputes now provide several new statusesPayments](/changelog/2014-08-20/disputes-provide-several-new-statuses)[Disputes now include multiple balance transactionsPayments](/changelog/2014-08-20/disputes-include-multiple-balance-transactions)

[2014-08-04](/changelog/2014-08-04)

Breaking changes

[You can now retrieve balance histories rather than relying on `Transfer` fieldsConnect](/changelog/2014-08-04/retrieve-balance-histories-transfer-fields)

[2014-07-26](/changelog/2014-07-26)

Breaking changes

[Application fees now include a sublist of refunds through the `refunds` fieldConnect](/changelog/2014-07-26/application-fees-include-refunds-sublist-refunds-field)

[2014-07-22](/changelog/2014-07-22)

[Invoice line items now include subscription plans and quantitiesInvoicing\+ 1 more](/changelog/2014-07-22/invoice-line-items-include-subscription-plans-quantities)

[2014-06-17](/changelog/2014-06-17)

Breaking changes

[Charges now include a sublist of refunds through the `refunds` fieldPayments](/changelog/2014-06-17/invoices-include-refunds-sublist-refunds-field)

[2014-06-13](/changelog/2014-06-13)

Breaking changes

[Renames the `type` field on cards to `brand`Payments\+ 1 more](/changelog/2014-06-13/renames-type-field-cards-brand)

[2014-05-19](/changelog/2014-05-19)

Breaking changes

[Replaces the `account` field on transfersConnect\+ 1 more](/changelog/2014-05-19/renames-account-field-transfers-bank-account)

[2014-03-28](/changelog/2014-03-28)

Breaking changes

[Lists no longer include the `count` fieldAffects all products](/changelog/2014-03-28/lists-no-longer-include-count-field)

[2014-03-13](/changelog/2014-03-13)

Breaking changes

[Renames the statement descriptor fieldConnect](/changelog/2014-03-13/renames-statement-descriptor-field-transfers)

[2014-01-31](/changelog/2014-01-31)

Breaking changes

[Customers now support multiple subscriptionsBilling](/changelog/2014-01-31/customers-support-multiple-subscriptions)[Trial end dates are no longer computed for canceled subscriptionsBilling](/changelog/2014-01-31/trial-end-dates-canceled-subscriptions)

## 2013

[2013-12-03](/changelog/2013-12-03)

Breaking changes

[Application fees now provide an expandable `account` field to obtain user detailsConnect](/changelog/2013-12-03/application-fees-provide-expandable-account-field)[Application fee refunds are now proportional to the charged amountConnect](/changelog/2013-12-03/application-fee-refunds-proportional-charged-amount)

[2013-10-29](/changelog/2013-10-29)

Breaking changes

[Coupons only apply to an invoice’s total balance, no longer applying to zero-cost invoicesInvoicing\+ 1 more](/changelog/2013-10-29/coupons-apply-invoice-total-balance)

[2013-08-13](/changelog/2013-08-13)

Breaking changes

[Fee details have moved from charges to their corresponding balance transactionsPayments](/changelog/2013-08-13/fee-details-moved-balance-transactions)[Fee details have moved from transfers to their corresponding balance transactionsPayments](/changelog/2013-08-13/fee-details-moved-balance-transactions-transfers)

[2013-08-12](/changelog/2013-08-12)

Breaking changes

[Lets the `description` and `email` fields be null on several objectsPayments\+ 2 more](/changelog/2013-08-12/allows-description-email-fields-null)

[2013-07-05](/changelog/2013-07-05)

Breaking changes

[Customers now include a `cards` sublist and `default_card` fieldPayments\+ 2 more](/changelog/2013-07-05/customers-include-cards-sublist-default-card-field)

[2013-02-13](/changelog/2013-02-13)

Breaking changes

[Disputes on charges are now tracked through the `stripe_fee` field and included in the fee totalPayments](/changelog/2013-02-13/disputes-tracked-stripe-fee-field-fee-total)

[2013-02-11](/changelog/2013-02-11)

Breaking changes

[Failed invoice payments now return an HTTP errorInvoicing\+ 1 more](/changelog/2013-02-11/failed-invoice-payments-return-http-error)

## 2012

[2012-11-07](/changelog/2012-11-07)

Breaking changes

[Renames the `disputed` field for Charges to `dispute`Payments](/changelog/2012-11-07/renames-disputed-field-charges-dispute)

[2012-10-26](/changelog/2012-10-26)

Breaking changes

[Invoices now include a sublist of invoice line itemsBilling\+ 1 more](/changelog/2012-10-26/invoices-include-invoice-line-items-sublist)

[2012-09-24](/changelog/2012-09-24)

Breaking changes

[Discounts no longer include an extraneous `id` fieldBilling\+ 1 more](/changelog/2012-09-24/discounts-no-longer-extraneous-id-field)

[2012-07-09](/changelog/2012-07-09)

Breaking changes

[Customers no longer include the `uncaptured` fieldPayments](/changelog/2012-07-09/customers-no-longer-uncaptured-field)

[2012-06-18](/changelog/2012-06-18)

Breaking changes

[Tokens no longer include the `amount` and `currency` propertiesElements\+ 1 more](/changelog/2012-06-18/tokens-no-longer-amount-currency-fields)

[2012-03-25](/changelog/2012-03-25)

Breaking changes

[Customers no longer include a `next_recurring_charge` fieldBilling](/changelog/2012-03-25/customers-no-longer-next-recurring-charge-field)

[2012-02-23](/changelog/2012-02-23)

Breaking changes

[Fields with null values are now included in API responsesAffects all products](/changelog/2012-02-23/fields-null-values-included-api-responses)

## 2011

[2011-09-15](/changelog/2011-09-15)

Breaking changes

[Cards validate differently when creating tokensElements\+ 1 more](/changelog/2011-09-15/cards-validate-differently-creating-tokens)

[2011-08-01](/changelog/2011-08-01)

Breaking changes

[Lists now provide a total count of items and a `data` fieldAffects all products](/changelog/2011-08-01/lists-provide-total-count-data-field)

[2011-06-28](/changelog/2011-06-28)

Breaking changes

[Plans no longer include the `identifier` fieldBilling](/changelog/2011-06-28/plans-no-longer-identifier-field)

[2011-06-21](/changelog/2011-06-21)

Breaking changes

[Errors now produce exceptions for unrecognized API parametersAffects all products](/changelog/2011-06-21/exceptions-unrecognized-api-parameters)