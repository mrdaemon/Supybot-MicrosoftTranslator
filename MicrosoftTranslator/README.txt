
Supybot-MicrosoftTranslator
============================

This is a supybot (limnoria, actually) plugin that allows you to translate text from and to a variety of languages.
It uses the Microsoft Translate Data Service on Azure Marketplace and as such, requires an Azure Marketplace key as
well as a (free) subscription to the service.

It was written because the translate API used by the translate function of the Google plugin was killed in favor of
the paid service known as Google Translate v2. Since we need to translate shit on our IRC channel at times, I stepped
up and wrote an almost transparent replacement that uses Microsoft's free-ish service. It works satisfyingly.

Setup
------

1) Register on the Azure Marketplace (https://datamarket.azure.com/)
2) Sign up for the Free 2 000 000 characters a month subscription for the Microsoft Translator service
   (https://datamarket.azure.com/dataset/1899a118-d202-492c-aa16-ba21c33c06cb)
3) Go to your account page and obtain your primary account key.
   (https://datamarket.azure.com/account/info)
4) Install and load the plugin
5) config conf.supybot.plugins.MicrosoftTranslator.azureKey your-azure-key
6) reload the plugin

Usage
------

translate <from_language> [to] <to_language> <text>
detect <text>

