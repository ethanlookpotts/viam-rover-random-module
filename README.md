# random modular service

This module provides a custom service to make your Viam rover drive with random movements.

This module implements the [rdk generic API](https://github.com/rdk/generic-api) in a ethanlook:rover:random model.

## Requirements

_Add instructions here for any requirements._

``` bash
```

## Build and Run

To use this module, follow these instructions to [add a module from the Viam Registry](https://docs.viam.com/registry/configure/#add-a-modular-resource-from-the-viam-registry) and select the `rdk:generic:ethanlook:rover:random` model from the [`ethanlook:rover:random` module](https://app.viam.com/module/rdk/ethanlook:rover:random).

## Configure your random rover service

> [!NOTE]  
> Before configuring your random rover service, you must [create a machine](https://docs.viam.com/manage/fleet/machines/#add-a-new-machine).

Navigate to the **Config** tab of your robot’s page in [the Viam app](https://app.viam.com/).
Click on the **Services** subtab and click **Create service**.
Select the `generic` type, then select the `ethanlook:rover:random` model. 
Enter a name for your generic and click **Create**.

On the new component panel, copy and paste the following attribute template into your generic’s **Attributes** box:

```json
{
  TODO: INSERT SAMPLE ATTRIBUTES
}
```

> [!NOTE]  
> For more information, see [Configure a Robot](https://docs.viam.com/manage/configuration/).

### Attributes

The following attributes are available for `rdk:generic:ethanlook:rover:random` generics:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `todo1` | string | **Required** |  TODO |
| `todo2` | string | Optional |  TODO |

### Example Configuration

```json
{
  TODO: INSERT SAMPLE CONFIGURATION(S)
}
```

### Usage

- To test your...
- To write code against your...

## Troubleshooting

_Add troubleshooting notes here._
