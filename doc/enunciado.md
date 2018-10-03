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

Cada ubicación pertenece a un único usuario. De la misma se registra un id, una descripción, una ubicación padre opcional (nula en caso de una ubicación raíz) y una o más imágenes (opcionales).

* Location:
  * Id
  * Parent
  * Description
  * Pictures
  * User

En cuanto a las categorías de ítems, éstas son codificadas, teniendo opcionalmente una imagen/ícono descriptiva de la misma, y permitiendo además la generación de categorías creadas por el usuario. Por lo tanto, de las mismas se registra un id, una descripción, una imagen/ícono (opcional) y un usuario creador (opcional).

* Category:
  * Id
  * Description
  * Picture
  * Creator

### Modelo de dominio

![modelo de dominio](http://www.plantuml.com/plantuml/svg/ZP7FIWCn4CRlUOfXZqBBBdYG8bBm97Zr0ORammxT_24pFOZuxYPTsQudlSnkPdvVyYCvgd6rIvpTIGB8I_Kpbly8E-MWpZazIofSELBA0Of23-EcMJcTU_D-TCxFh4flYagVZaX2AuaZsWUHPNPVFyYB8TwG0FLLYabERLN4swL2L_WrU-wpVmUUsV2UwySVWSPVLOTfe1qDTyEYTQ2I5Q2dpNGPho87uX0bYLhbnlLO0nPk-iKzai_910bkxNQoWUD-Fz6kS4MoMyQjyXjiMEwqRuSWnfiJhtNDD7TKGuBl_aUaq1xt6m00)
