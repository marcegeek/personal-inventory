# Inventario de objetos personales - Personal Inventory

El sistema a desarrollar se trata de una aplicación Web que permita a los usuarios gestionar los distintos objetos personales (ítems) que posean.

Se debe permitir gestionar la ubicación de los mismos en las distintas ubicaciones que el usuario indique.

## Modelado del dominio

Cada ítem pertenece a un único usuario y se localiza en una ubicación. Del mismo se conocen un id y una descripción.

Algunos ítems pueden además ser no-atómicos, es decir, están formados por muchos ítems pequeños e idénticos que se manejan como si fueran uno solo (ej.: agujas, alfileres, clavos, etc.). En este caso, se registra la cantidad actual del mismo.

* ItemModel:
  * Id
  * Description
  * LocationModel
  * UserModel

* NonAtomicItemModel: ItemModel
  * Quantity

De cada usuario se registra un id, el nombre y apellido, un e-mail y el nombre de usuario.

* UserModel:
  * Id
  * FirstName
  * LastName
  * Email
  * Username

Cada ubicación pertenece a un único usuario. De la misma se registra un id y una descripción.

* LocationModel:
  * Id
  * Description
  * UserModel

### Modelo de dominio

![modelo de dominio](http://www.plantuml.com/plantuml/svg/TKuzImGn4EtpAuOjXOCJBEGAEKj1x6o58HcvuJAJDJCfHFplPdSbfuXDydWVRzxH7AitoU74YI1oZPasBEIdaYo4O6VM6IiAQ4baDCFj_WTPKSyBURCF8MOqWsUZ2Xy1W5D_NhcQAmfrd7504kJS_zRDA_NvdNvmaakw7uoLP-UYm_5KzDwBS1pMjuRgxE_3ybWYBfd_YjQ9q_K4knrCLzDsz01pCIAukyYREjeEW4bOsRnYjmt-RrCiVH3fKhOoBrt-jJiSILEJ_0K0)

### Diagrama Entidad-Relación

![diagrama entidad relación](er.svg)
