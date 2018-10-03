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

![modelo de dominio](http://www.plantuml.com/plantuml/svg/XP6_QWCn3CPtFuNmM4X8e4CvIWbqAdJj0mXRD2BdFrZAK4hVlRfpSQvJ5ftkq--pFkoJA3QzfjcTEH84Rc6ctYVISudYd9CBvueD4-GIIQZ2qs4ZDioNHNmyE1Tc584FeGRV3e2ZbOo9x4C9UNO_VyYRKheXaIGqhiebsr_beDT6Ocr0fS_Ic6Gutuk91jvp3yDhF-FhZi7uDRS_UjY1V_0zumIr216yRAPzF89CW35nPj66nYqs0pft_CU5afKfar53NKdmX_t-2BkAZRBUF6w4ts2-N_04pq2H5JSRrpeybfsQKgQmR3nHZlRIlm00)
