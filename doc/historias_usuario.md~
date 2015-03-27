# Historia Gestionar Región Académica

+ **COD**: 0001
+ **Nombre**: Gestionar Región Académica
+ **Descripción**: El sistema debe poder adicionar, modificar y eliminar las Regiones Académicas. En un principio el sistema debe tener 7 RA. Las mismas poseen un código y están constituidas por varias provincias. RA I (código: 01; provincias: Luanda y Bengo), RA II (02; Benguela y Kwanza Sul), RA III (03; Cabinda y Zaire), RA IV (04; Lunda Norte, Lunda Sul y Malanje), RA V (05; Huambo, Bié y Moxico), RA VI (06; Huíla, Namibe, Cunene y Cuando Cubango) y RA VII (07; Uíge y Kwanza Norte). Si bien está definido en la educación superior de angola que son estas y solo estas regiones, existe la posibilidad de variaciones en ellas. 
+ **¿Cómo probarlo?**: Al adicionar, modificar o eliminar una Región Académica se debe modificar la BD con el respectivo cambio.

# Historia Gestionar IES

+ **COD**: 0002
+ **Nombre**: Gestionar IES
+ **Descripción**: El sistema debe poder adicionar, modificar y eliminar los IES. Los Institutos de la Enseñanza Superior en Angola pertenecen a una de las Regiones Académicas existentes. Poseen una clasificación con su respectivo código. Universidades (10), Institutos Superiores (20), Institutos Superior Técnicos (21), Institutos Superior Politécnicos (22), Escolas Superior (30), Escolas Superior Técnicas (31), Escola Superior Politécnicas (32), Academias (40) y Centros de Investigação Científica (70). Además tienen una naturaleza, con su respectivo codificación; la misma consiste en Pública (1), Privada (2) y Público-Privada (3). También poseen un código de registro del IES, que está compuesto por todos los códigos antes mencionados y otros 3 en dependencia del registro. Por ejemplo, si la Universidade Kimpa Vita fuese la octava IES a ser registrada en el Ministerio entonces su código seria 07101008 siendo 07 el código de la respectiva Región Académica, 10 o código de clasificación de la IES que en este caso es una Universidad, 1 la naturaleza de la IES en este caso pública y 008 el número secuencial indicando que fuela octava IES a ser registada en el Ministerior. También poseen un logotipo (imagen), la cual se utilizará para todos los documentos generados del sistema. El sistema no generará o asignará código alguno a los IES, los códigos de los IES ya están definidos por el Ministerio. El sistema solo los gestionará.
+ **¿Cómo probarlo?**: Al adicionar, modificar o eliminar un IES se debe modificar la BD con el respectivo cambio.

# Historia Gestionar Unidades Orgánicas (UO)

+ **COD**: 0003
+ **Nombre**: Gestionar Unidades Orgánicas (UO)
+ **Descripción**: El sistema debe poder adicionar, modificar y eliminar las UO. Las UO pertenecen a alguno de los IES. Poseen un nivel de agregación con su respectiva codificación, Sede Central (1) y Unidad orgánica (2). Poseen una clasificación de la Unidad Orgánica con su respectiva codificación, Institutos Superior (20), Institutos Superior Técnico (21), Institutos Superior Politécnicos (22), Escolas Superior (30), Escolas Superior Técnicas (31), Escolas Superior Politécnicas (32), Academias (40), Faculdades (50), Departamentos (60) y Centros de Investigação Científica (70). Las UO poseen un código de registro que está compuesto por 14 caracteres (los primeros 8 es el código del IES al que pertenece, luego 1 caracter correspondiente al nivel de agregación, luego 2 caracteres correspondientes a la clasificación y finalmente otros 3 que representan un número sequencial/consecutivo; el criterio utilizado para conformar este campo es el orden de registro de la unidad orgânica en el minesterio. Además las UO poseen un código adicional que es asignado por el IES al que pertenece, este código posee 2 caracteres, por ejemplo 01.  Nota: todos esos datos la primera ves que se ejecute la aplicación - aunque el usuario tenga la posibilidad de gestionar esos datos despues - lo que estoy pensando es que como es raro que se cambie de UO en el centro de educación donde se esta usando el sistema esa parte de seleccionar UO se puede poner como parte tambien de la configuración, por ejemplo fijar en db.py o en otra parte una constante con el ID de la unidad organica con la que se esta trabajando en esa instalación.
+ **¿Cómo probarlo?**: Al adicionar, modificar o eliminar una UO se debe modificar la BD con el respectivo cambio.

# Historia Seleccionar Unidad Orgánica (UO)

+ **COD**: 0004
+ **Nombre**: Seleccionar Unidad Orgánica (UO)
+ **Descripción**: El sistema deberá permitir escoger la Unidad Orgánica donde se trabajará. 
+ **¿Cómo probarlo?**: 

# Historia Gestionar Cursos

+ **COD**: 0005
+ **Nombre**: Gestionar Cursos
+ **Descripción**: El sistema debe poder adicionar, modificar y eliminar las cursos a impartir en la UO seleccionada. Los cursos tienen o perteneces a un área del conocimiento según el ministerio y su código (1 caracter) correspondiente, un área del conocimiento según el Plan Nacional de Formación de Quadro y su código (2 caraceres) correspondiente, un grupo de sectores de la UNESCO y su código (3 caracteres) correspondiente, un código de registro conformado por 9 caracteres (1:código de área del conocimeineto según ministerio; 2:código del área del conocimiento según PNFQ; 3:código del sector de la UNESCO y 3:números consecutivos y secuenciales) y un código asignado por el IES al que pertenece la UO que impartirá el curso.
+ **¿Cómo probarlo?**: Al adicionar, modificar o eliminar un Curso se debe modificar la BD con el respectivo cambio.

# Historia Gestionar Régimes

+ **COD**: 0006
+ **Nombre**: Gestionar Régimes
+ **Descripción**: El sistema debe poder adicionar, modificar y eliminar los régimes. Por defecto tendrá 2 régimes (Regular y Post-Laboral). Los régimenes poseen un nombre y una abreviatura.
+ **¿Cómo probarlo?**: Al adicionar, modificar o eliminar un Régime se debe modificar la BD con el respectivo cambio.

# Historia Gestionar Régimes

+ **COD**: 0007
+ **Nombre**: Gestionar Régimes
+ **Descripción**: El sistema debe poder adicionar, modificar y eliminar los régimes. Por defecto tendrá 2 régimes (Regular y Post-Laboral). Los régimenes poseen un nombre y una abreviatura.
+ **¿Cómo probarlo?**: Al adicionar, modificar o eliminar un Régime se debe modificar la BD con el respectivo cambio.

# Historia Gestionar Año Académico

+ **COD**: 0008
+ **Nombre**: Gestionar Año Académico
+ **Descripción**: El sistema debe poder adicionar, modificar y eliminar los Años Académicos. Los Años Académicos tienen un año y una descripción. Los años académicos en Angola comienzan en febrero y terminan en diciembre.
+ **¿Cómo probarlo?**: Al adicionar, modificar o eliminar un Año Académico se debe modificar la BD con el respectivo cambio.

# Historia Gestionar Candidatos

+ **COD**: 0009
+ **Nombre**: Gestionar Candidatos
+ **Descripción**: El sistema debe poder adicionar, modificar y eliminar a los candidatos a ingresar a la Enseñanza Superior, en este caso a la Unidad Orgánica que se creó con anterioridad. Los datos necesarios de los candidatos son los siguientes: Prefijo (Señor o Señora), Usuario de acceso al sistema, Contraseña de acceso al sistema, Nombre completo (65 caracteres), Fecha de nacimiento (10 dígitos), Género (1 dígito) con su código correspondiente (Masculino:1 ; Femenino:2) , Estado civil (1 dígito; Casado:1; Soltero:2; Divorciado:3; Otro:4), Tipo de documento de identidad, Número de Documento de identidad, Fecha de emisión del Documento de identidad, Entidad que emitió el Documento de identidad, Nombre del padre, Nombre de la madre, Natural de (Municipio), Nacionalidad (se seleccionará uno de todos los países existentes), Habilitación (esto es el grado anterior logrado 11no, 12º ect), Procedencia Escolar de Enseñanza Media (1 dígito), Escuela de procedencia, Curso de Procedencia (20 caracteres), Año de conclusión, Estatus (Civil, Militaro o Policía), Condición (Estudiante trabajador o No trabajador), Nombre del trabajo (20 caracteres), Profesión, Provincia, Necesidad de educación especial, Estado (Activo e Inactivo), Procesos que posee (Certificado original, Cópia de documento, Documento de trabajo, Documento Militar, Internato), Dirección particular incluyendo comuna, Teléfono, Curso a lo que se candidata (pueden ser hasta 2 de los que se imparten en la UO y deben elegirse en orden de prioridad), Forma de pago (TPA, Novo bordereaux) en ambos casos se tiene la cantidad y en el caso específico del bordereaux tiene un número, Número de expediente (4 dígitos) corresponde al orden de inserción de este candidato, email, Nombre del curso de procedencia en la enseñaza media (20 caracteres), Nota de examen de acceso (en base a 20), Admitido (1:Si; 0:No), Matriculados por primera ves (1:Si; 0:No), Regimen. 
+ **¿Cómo probarlo?**: Al adicionar, modificar o eliminar un Candidato se debe modificar la BD con el respectivo cambio.

# Historia Gestionar Municipios

+ **COD**: 0010
+ **Nombre**: Gestionar Municipios
+ **Descripción**: El sistema debe poder adicionar, modificar y eliminar Municipios. Los Municipios tienen un nombre y un código (6 dígitos). También pertenecen a una provincia.
+ **¿Cómo probarlo?**: Al adicionar, modificar o eliminar un Municipio se debe modificar la BD con el respectivo cambio.

# Historia Gestionar Comuna

+ **COD**: 0011
+ **Nombre**: Gestionar Comuna
+ **Descripción**: El sistema debe poder adicionar, modificar y eliminar las Comunas. Las Comunas tienen un nombre y pertenecen a un municipio.
+ **¿Cómo probarlo?**: Al adicionar, modificar o eliminar una Comuna se debe modificar la BD con el respectivo cambio.

# Historia Adicionar Código a las Provincia

+ **COD**: 0012
+ **Nombre**: Adicionar Código a las Provincia
+ **Descripción**: Las provincias tienen un código (2 dígitos).
+ **¿Cómo probarlo?**: Al adicionar, modificar o eliminar una Província se debe modificar la BD con el respectivo cambio.

# Historia Gestionar Necesidad de Educación Especial

+ **COD**: 0013
+ **Nombre**: Gestionar Necesidad de Educación Especial
+ **Descripción**: El sistema debe poder adicionar, modificar y eliminar las Necesidad de Educación Especial. Una Necesidad de Educación Especial tienen un nombre y un código (1 dígito).
+ **¿Cómo probarlo?**: Al adicionar, modificar o eliminar una Necesidad de Educación Especial, se debe modificar la BD con el respectivo cambio.

# Historia Gestionar Procedencia Escolar de Enseñanza Media

+ **COD**: 0014
+ **Nombre**: Gestionar Procedencia Escolar de Enseñanza Media
+ **Descripción**: El sistema debe poder adicionar, modificar y eliminar las Procedencias Escolar de Enseñanza Media. Una Procedencia Escolar de Enseñanza Media tienen un nombre y un código (1 dígito).
+ **¿Cómo probarlo?**: Al adicionar, modificar o eliminar una Procedencia Escolar de Enseñanza Media, se debe modificar la BD con el respectivo cambio.


