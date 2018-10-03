# Inventario de objetos personales - Personal Inventory

El sistema a desarrollar se trata de una aplicación Web que permita a los usuarios gestionar los distintos objetos personales (ítems) que posean.

Se debe permitir gestionar la ubicación de los mismos en las distintas ubicaciones que el usuario indique. Permitiendo además el anidamiento de tales ubicaciones en estructura de árbol.

Se debe poder además registrar múltiples ubicaciones raiz (ej: casa, trabajo, entre otras).

También se quiere llevar un registro temporal del uso de tales ítems para poder realizar estadísticas como pueden ser por ejemplo, ítems que no se utilizan hace X tiempo.

## Modelado del dominio

Cada ítem pertenece a un único usuario y se localiza en una ubicación. Del mismo se conocen un id, una descripción y una o más imágenes (opcionales). También se registran opcionalmente varias categorías (etiquetas, sin jerarquía) para el mismo.

* Item:
  * Id
  * Description
  * Pictures
  * Categories
  * Location
  * User

De cada usuario se registra un id, un nombre y un e-mail.

* User
  * Id
  * Name
  * Email

De las ubicaciones se registra un id, una descripción, una ubicación padre opcional (nula en caso de una ubicación raíz) y una o más imágenes (opcionales).

* Location:
  * Id
  * Parent
  * Description
  * Pictures

En cuanto a las categorías de ítems, éstas son codificadas, teniendo opcionalmente una imagen/ícono descriptiva de la misma, y permitiendo además la generación de categorías creadas por el usuario. Por lo tanto, de las mismas se registra un id, una descripción, una imagen/ícono (opcional) y un usuario creador (opcional).

* Category:
  * Id
  * Description
  * Picture
  * Creator

### Modelo de dominio

![modelo de dominio](http://www.plantuml.com/plantuml/svg/XO-zQWGn38HxFuNOCh17hZr2E4WLI9i7CFQG4wn_aBH527dts7i_JaXnZIrxlXb9HpKljgR5dJY20ajOSAuJx5IYEXSMhqhl2g4lHyIn7Tadj0l9y-A-ByYh8GqaGeDmDIwvlIe7MmNQok0D7qKOUdE-bU0xUCSz32_dZCyxXiQxRQhfOQ9vfca_ZLu7Ug9GiZ4oN5zla-UDxQO6rA80FVzIk_mdmyV4cTN4D-xsV-ttkDljQQvUa6tOBdbTl4QEZGw4oDRJnkJ_a0enP0Gqx8WSrxJy0000)
