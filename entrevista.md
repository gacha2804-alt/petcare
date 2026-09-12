Doctor Andrés, Más que hacerle una entrevista formal, quisiera conversar un poco sobre cómo trabajan actualmente en la clínica. 
La idea es entender qué cosas les funcionan bien, qué cosas les generan dificultades y, a partir de eso, mirar en qué podría
ayudar una aplicación como PetCare.
Para empezar, cuénteme un poco, ¿cómo es el día a día en la clínica y cómo manejan actualmente la información de las mascotas?

*Respuesta doc*: Mira, te cuento cómo es la cosa por acá.
Ahorita mismo trabajamos con un sistema mitad y mitad, la verdad.
Tenemos un software de escritorio para las historias clínicas —uno que instalamos hace como 6 años— pero para las citas usamos una agenda de Google Calendar 
que maneja mi secretaria, y para recordarle a los dueños de las mascotas las vacunas o los controles, honestamente, eso lo hacemos por WhatsApp, uno por uno,
cuando nos acordamos.
El problema es que esos tres sistemas no se hablan entre sí. Si un cliente llama y pregunta "¿cuándo le toca la próxima vacuna a mi perro?",
mi secretaria tiene que ir al software de escritorio, buscar el paciente, revisar el historial, y de ahí calcular manualmente cuándo es la próxima dosis.
Eso nos quita tiempo que podríamos usar atendiendo.
Otra cosa que nos pasa mucho: la gente no llega a las citas o llega tarde y no avisa, y eso nos descuadra toda la agenda del día. Y cuando tenemos dos sedes, 
a veces un cliente lleva a su mascota a la sede A pero el historial completo solo lo tenemos actualizado en la sede B, porque el software no sincroniza bien entre las dos.
Lo que sí nos funciona bien es la parte de facturación, la verdad, y el manejo del inventario de medicamentos —eso lo tenemos bastante controlado con otro sistema aparte.
¿Eso te sirve como punto de partida? Cuéntame, ¿por dónde quieres seguir indagando?

Sí, doctor, me sirve mucho como punto de partida. Me gustaría entender un poco más los procesos que actualmente les generan más dificultad en el día a día.
Por ejemplo, pensando en una jornada normal de trabajo, ¿hay algún proceso que sientan que les quita bastante tiempo o que todavía
tengan que hacer de manera manual? Cuéntame un poco cómo lo manejan actualmente y qué es lo que más se les dificulta.

*Respuesta doc*: Los procesos que más se nos dificultan son:

Recordatorios de vacunas/desparasitación — todo manual, mi secretaria revisa historial por historial cada semana.
Confirmación de citas — no hay recordatorio automático, por eso tenemos bastantes "no-shows".
Historial disperso entre sedes — si el paciente viene de la otra sede, toca llamar o esperar fotos por WhatsApp.
Registro de consultas — el veterinario digita todo después, entre paciente y paciente, y a veces se le olvidan detalles.
Acceso del cliente a su información — no tienen dónde ver historial, exámenes o fórmulas; todo se pierde en WhatsApp o papel.

Me parece muy útil lo que me cuentas. Creo que podríamos empezar por los recordatorios de vacunas y desparasitación, 
porque veo que actualmente es un proceso bastante manual.
Si pudiéramos automatizar ese proceso, ¿cómo te gustaría que funcionara? Por ejemplo, ¿que el sistema detecte automáticamente las fechas próximas, 
le avise a tu secretaria y además envíe un recordatorio al propietario?

*Respuesta doc*: Me gustaría que funcionara así:
1. Que el sistema calcule solo las fechas. Cuando el veterinario aplica una vacuna o una desparasitación, que quede registrado en el sistema
y que automáticamente calcule cuándo toca la próxima dosis, según el tipo de producto y el protocolo que nosotros definamos. 
no dependemos de que alguien se acuerde de hacer la cuenta.
2. Que le avise primero a mi equipo, no directo al cliente.
Me gustaría que unos días antes —digamos una semana— le llegue una alerta a mi secretaria con la lista de mascotas a las que les toca algo esa semana
para que ella revise y confirme que todo esté bien antes de que se dispare el mensaje al dueño.
No quiero que el sistema le escriba solo a la gente sin que nosotros tengamos control de eso.
3. Que el recordatorio al propietario sea automático pero editable. Que se le envíe un mensaje —por WhatsApp o notificación de la app,
lo que sea más efectivo— avisándole que a su mascota le toca tal vacuna en tal fecha, y que le permita agendar la cita directamente desde ahí,sin tener que llamarnos.
4. Que si el cliente no responde o no agenda, el sistema insista. Un segundo recordatorio a los pocos días si no ha habido respuesta,
porque muchas veces la gente ve el mensaje y se le olvida.
5. Y algo importante para mí: que quede un reporte. Quiero poder ver, por ejemplo, cuántas mascotas tenían algo pendiente ese mes, cuántas se pusieron al día y
cuántas quedaron sin atender, para hacerle seguimiento desde la gerencia.

Sí, doctor, con eso ya me queda mucho más claro el flujo que tienen en mente. 
Para aterrizarlo un poco más, cuando el veterinario registra una vacuna o una desparasitación, ¿qué información suelen registrar ustedes en ese momento? Por ejemplo,
el nombre del producto, la fecha, la dosis, el fabricante o algún otro dato que consideren importante.
Me interesa saber qué información debería tener el sistema para poder calcular correctamente la próxima fecha.

*Respuesta doc*:Buena pregunta, eso es clave para que el cálculo salga bien. Te cuento lo que normalmente registramos:
Nombre comercial del producto (ej. Nobivac, Vanguard, etc.) y tipo de vacuna o antiparasitario — porque no es lo mismo la polivalente que la antirrábica,
cada una tiene su propio esquema.
Fabricante y número de lote — esto es importante para nosotros por trazabilidad, sobre todo si algún día hay una alerta sanitaria de algún lote específico.
Fecha de aplicación — obvio, es la base para calcular todo.
Dosis aplicada (en ml o mg, según el producto) y vía de aplicación (subcutánea, intramuscular, etc.).
Peso del paciente en el momento de la aplicación — porque muchas dosis, sobre todo de antiparasitarios, dependen del peso,
y además nos sirve para ver la evolución del animal.
Edad del paciente — porque el esquema no es igual para un cachorro que para un adulto; los cachorros llevan varias dosis de refuerzo seguidas.
Veterinario que la aplicó — para responsabilidad profesional, por si hay alguna reacción adversa hay que saber quién fue.
Reacciones o novedades — un campo abierto por si el animal tuvo alguna reacción alérgica o algo raro, para tenerlo en cuenta la próxima vez.
Y lo que necesitaría el sistema para el cálculo automático, específicamente, es que nosotros podamos definir de antemano 
el protocolo por tipo de producto y por especie —por ejemplo "vacuna X en perros: refuerzo cada 12 meses, 
pero en cachorros menores de 4 meses cada 21 días"— para que el sistema no calcule igual a todos los pacientes.
¿Te sirve así, o quieres que profundicemos en algún dato en particular? 

Sí, doctor, perfecto. Con eso ya tengo bastante claro qué información debería manejar el sistema y cómo debería funcionar el cálculo automático. 
Para no quitarte demasiado tiempo, me gustaría pasar al otro problema que mencionaste: Perfecto, doctor. Ya entiendo cómo están trabajando actualmente
y también qué partes no sería necesario tocar porque ya les funcionan bien, como facturación e inventario.
Entonces, pensando específicamente en las citas y esos pacientes que no se presentan, ¿qué te gustaría que PetCare hiciera para reducir ese problema? 
Por ejemplo, ¿te bastaría con que enviara recordatorios y permitiera confirmar la cita, o te gustaría que también manejara cancelaciones,
reprogramaciones y los espacios que quedan disponibles?

*Respuesta doc*: Con solo el recordatorio no me basta, porque el problema no es que la gente se le olvide nada más, sino que cuando cancela,
cancela tarde o no avisa, y esa hora ya no la puedo recuperar. Entonces me gustaría que fuera un poquito más completo:
1. Recordatorio con confirmación activa. Que le llegue el mensaje uno o dos días antes y que el cliente tenga que confirmar con un botón —"Sí, voy" o "No puedo asistir"— no que sea solo informativo. Así yo sé de verdad quién va a llegar.
2. Que permita reprogramar directo desde ahí. Si el cliente dice que no puede, que la misma app le muestre los horarios disponibles esa semana y pueda mover la cita él mismo, sin tener que llamarnos.
3. Que libere el cupo automáticamente. En el momento en que alguien cancela o no confirma en cierto tiempo —digamos, si no confirma 12 horas antes—, que ese espacio quede visible como disponible para que otro cliente lo pueda tomar, incluso alguien que esté buscando cita de urgencia.
4. Una lista de espera. Esto me interesa mucho: que si un horario está lleno, el cliente pueda anotarse en lista de espera, y si alguien cancela, que automáticamente se le avise al primero de la lista.
5. Y para nosotros, del lado administrativo: un tablero donde mi secretaria vea de un vistazo cuáles citas del día ya están confirmadas, cuáles pendientes y cuáles canceladas, para poder gestionar mejor el día sin tener que llamar uno por uno a preguntar.
Lo que sí te pido es que sea simple para el cliente, porque muchos de mis pacientes... digo, los dueños de mis pacientes, ¡ja!, no son tan hábiles con la tecnología, entonces si el proceso de confirmar o reprogramar es muy enredado,
van a terminar llamando de todas formas.

Perfecto, doctor. Muchas gracias por explicarme todo con tanto detalle y por tomarte el tiempo para contarme cómo trabajan actualmente y qué cosas te gustaría mejorar.

Con todo lo que me has contado ya tengo una visión mucho más clara de las necesidades de la clínica, especialmente en temas como el seguimiento de vacunas y desparasitación, las citas, 
la comunicación con los propietarios y la información entre las dos sedes.

