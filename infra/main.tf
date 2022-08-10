provider "azurerm" {
  features {
  }
}

resource "azurerm_resource_group" "default" {
  name     = "rg-function-app"
  location = "Germany West Central"
}

resource "random_string" "unique" {
  length  = 8
  upper   = false
  special = false
}

resource "azurerm_storage_account" "default" {
  name                     = "storage${random_string.unique.result}"
  resource_group_name      = azurerm_resource_group.default.name
  location                 = azurerm_resource_group.default.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_service_plan" "default" {
  name                = "azure-functions-service-plan"
  location            = azurerm_resource_group.default.location
  resource_group_name = azurerm_resource_group.default.name

  os_type  = "Linux"
  sku_name = "S1"

}

resource "azurerm_linux_function_app" "default" {
  name                       = "depgate-function-app-${random_string.unique.result}"
  location                   = azurerm_resource_group.default.location
  resource_group_name        = azurerm_resource_group.default.name
  service_plan_id            = azurerm_service_plan.default.id
  storage_account_name       = azurerm_storage_account.default.name
  storage_account_access_key = azurerm_storage_account.default.primary_access_key

  site_config {
    application_stack {
      python_version = "3.9"
    }
  }
}

