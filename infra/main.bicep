
param env string
param location string = resourceGroup().location
param sqlAdminUser string = 'sqladminuser'
@secure()
param sqlAdminPass string

var namePrefix = 'ass-${env}' // azure-sensor-streaming

resource kv 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: '${namePrefix}-kv'
  location: location
  properties: {
    tenantId: subscription().tenantId
    sku: { family: 'A'; name: 'standard' }
    enablePurgeProtection: true
    enableSoftDelete: true
  }
}

resource ai 'Microsoft.Insights/components@2020-02-02' = {
  name: '${namePrefix}-appi'
  location: location
  kind: 'web'
  properties: { Application_Type: 'web' }
}

resource plan 'Microsoft.Web/serverfarms@2022-09-01' = {
  name: '${namePrefix}-plan'
  location: location
  sku: { name: 'P1v2', capacity: 1, tier: 'PremiumV2' }
}

resource api 'Microsoft.Web/sites@2022-09-01' = {
  name: '${namePrefix}-api'
  location: location
  kind: 'app'
  properties: {
    httpsOnly: true
    siteConfig: {
      appSettings: [
        { name: 'WEBSITE_RUN_FROM_PACKAGE'; value: '1' }
        { name: 'APPINSIGHTS_INSTRUMENTATIONKEY'; value: ai.properties.InstrumentationKey }
      ]
    }
  }
  sku: { name: 'P1v2'; tier: 'PremiumV2' }
  dependsOn: [ plan ]
}

resource func 'Microsoft.Web/sites@2022-09-01' = {
  name: '${namePrefix}-fn'
  location: location
  kind: 'functionapp,linux'
  properties: {
    httpsOnly: true
    siteConfig: {
      appSettings: [
        { name: 'WEBSITE_RUN_FROM_PACKAGE'; value: '1' }
        { name: 'FUNCTIONS_WORKER_RUNTIME'; value: 'dotnet-isolated' }
        { name: 'APPINSIGHTS_INSTRUMENTATIONKEY'; value: ai.properties.InstrumentationKey }
      ]
      linuxFxVersion: 'DOTNET|8.0'
    }
  }
  sku: { name: 'P1v2'; tier: 'PremiumV2' }
  dependsOn: [ plan ]
}

resource st 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: replace(toLower('${namePrefix}st'), '-', '')
  location: location
  sku: { name: 'Standard_LRS' }
  kind: 'StorageV2'
  properties: { allowBlobPublicAccess: false }
}

resource evhns 'Microsoft.EventHub/namespaces@2022-01-01-preview' = {
  name: '${namePrefix}-ehns'
  location: location
  sku: { name: 'Standard'; tier: 'Standard' }
}

resource evh 'Microsoft.EventHub/namespaces/eventhubs@2022-01-01-preview' = {
  name: '${evhns.name}/events'
  properties: { messageRetentionInDays: 1; partitionCount: 2 }
}

resource sql 'Microsoft.Sql/servers@2021-11-01-preview' = {
  name: '${namePrefix}-sql'
  location: location
  properties: {
    administratorLogin: sqlAdminUser
    administratorLoginPassword: sqlAdminPass
    publicNetworkAccess: 'Enabled'
  }
}

resource sqldb 'Microsoft.Sql/servers/databases@2021-11-01-preview' = {
  name: '${sql.name}/${namePrefix}-db'
  sku: { name: 'S0'; tier: 'Standard' }
  properties: { catalogCollation: 'SQL_Latin1_General_CP1_CI_AS' }
}

output apiName string = api.name
output functionName string = func.name
output eventHub string = evh.name
output sqlServer string = sql.name
output sqlDb string = sqldb.name
output storage string = st.name
