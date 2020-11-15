PAV - P3: detección de pitch
============================

Esta práctica se distribuye a través del repositorio GitHub [Práctica 3](https://github.com/albino-pav/P3).
Siga las instrucciones de la [Práctica 2](https://github.com/albino-pav/P2) para realizar un `fork` de la
misma y distribuir copias locales (*clones*) del mismo a los distintos integrantes del grupo de prácticas.

Recuerde realizar el *pull request* al repositorio original una vez completada la práctica.

Ejercicios básicos
------------------

- Complete el código de los ficheros necesarios para realizar la detección de pitch usando el programa
  `get_pitch`.

   * Complete el cálculo de la autocorrelación e inserte a continuación el código correspondiente.

   ```c++
     void PitchAnalyzer::autocorrelation(const vector<float> &x, vector<float> &r) const {
    
    for (unsigned int l = 0; l < r.size(); ++l) {
  		/// \TODO Compute the autocorrelation r[l]
      for(unsigned int i = 0; i < x.size()-l; ++i){
        r[l] += x[i]*x[i+l];
      }
      r[l] = (1.0F/x.size())*r[l];
    }
      /// \DONE Implementado el calculo de la autocorrelación.
    if (r[0] == 0.0F) //to avoid log() and divide zero 
      r[0] = 1e-10; 
  }
  ```

   * Inserte una gŕafica donde, en un *subplot*, se vea con claridad la señal temporal de un segmento de
     unos 30 ms de un fonema sonoro y su periodo de pitch; y, en otro *subplot*, se vea con claridad la
	 autocorrelación de la señal y la posición del primer máximo secundario.

	 NOTA: es más que probable que tenga que usar Python, Octave/MATLAB u otro programa semejante para
	 hacerlo. Se valorará la utilización de la librería matplotlib de Python.

   <img src="ac_plot.png" width="640" align="center">

   Para generar esta gráfica hemos creado un script `ac_plot.py` ubicado dentro de la carpeta scripts. En 
   este script representamos una trama de señal sonora del archivo `test_pitch.wav` y su autocorrelación. Esta 
   trama ha sido encontrada de manera manual (escuchando el audio).

   * Determine el mejor candidato para el periodo de pitch localizando el primer máximo secundario de la
     autocorrelación. Inserte a continuación el código correspondiente.

     ```c++
      while(*iR > 0 && iR != r.end()){
      ++iR;
      }

      if (iR == r.end()){
        iRMax = r.begin() + npitch_max;
      } else {

        if (iR < r.begin() + npitch_min) {
        iR = r.begin() + npitch_min;
        }

        iRMax = iR;

        while (iR != r.end()) {
          if (*iR > *iRMax) {
            iRMax = iR;
          }
          ++iR;
        }
      }
     ```

   * Implemente la regla de decisión sonoro o sordo e inserte el código correspondiente.

   ```c++
    bool PitchAnalyzer::unvoiced(float pot, float r1norm, float rmaxnorm) const {
    /// \TODO Implement a rule to decide whether the sound is voiced or not.
    /// * You can use the standard features (pot, r1norm, rmaxnorm),
    ///   or compute and use other ones.
    return (pot < -40.0F || r1norm <= 0.92F) && rmaxnorm <= 0.53F;
    /// \DONE Decision de sordo/sonoro implementada. Usamos pot = -40, r1norm = 0,92 y rmaxnorm = 0,53.
    }
   ```
   Usamos la potencia de la señal, el valor de r1 normalizado y el valor de rmax normalizado. Los valores que aperecen en el código los hemos obtenido a posteriori.

- Una vez completados los puntos anteriores, dispondrá de una primera versión del detector de pitch. El 
  resto del trabajo consiste, básicamente, en obtener las mejores prestaciones posibles con él.

  * Utilice el programa `wavesurfer` para analizar las condiciones apropiadas para determinar si un
    segmento es sonoro o sordo. 
	
	  - Inserte una gráfica con la detección de pitch incorporada a `wavesurfer` y, junto a ella, los 
	    principales candidatos para determinar la sonoridad de la voz: el nivel de potencia de la señal
		(r[0]), la autocorrelación normalizada de uno (r1norm = r[1] / r[0]) y el valor de la
		autocorrelación en su máximo secundario (rmaxnorm = r[lag] / r[0]).

		Puede considerar, también, la conveniencia de usar la tasa de cruces por cero.

	    Recuerde configurar los paneles de datos para que el desplazamiento de ventana sea el adecuado, que
		en esta práctica es de 15 ms.

    <img src="grafica1_wavesurfer.png" width="640" align="center">

    En esta grafica se puede observar, en este orden y de arriba a abajo, la correlación máxima normalizada, 
    la correlación en k=1 normalizada, la potencia de la señal, el valor de pitch calculado por wavesurfer y 
    la señan analizada, "test_pitch.wav".

    A partir de aquí procedemos a investigar qué valores de cada gráfica determinan si una trama sera sorda o 
    sonora. Despúes de analizar las gráficas, llegamos a la conclusión de que todas las tramas sordas tienen 
    una correlación máxima inferior a ~ 0,5. Pero esto no es motivo suficiente para determinar la sonoridad de 
    la trama. Además, tiene que cumplir que la potencia de la señal es baja, inferior a ~ -40 dB o en su defecto
    que la correlación en k=1 sea inferior a ~ 0,9. Si no cumple ninguna de las condiciones anteriores, significa 
    que la trama es sonora y podemos proceder a calcular el pitch.

      - Use el detector de pitch implementado en el programa `wavesurfer` en una señal de prueba y compare
	    su resultado con el obtenido por la mejor versión de su propio sistema.  Inserte una gráfica
		ilustrativa del resultado de ambos detectores.

    <img src="grafica2_wavesurfer.png" width="640" align="center">

    Nuestro detector de pitch creemos que es bastante bueno. El valor del pitch que calcula es muy parecido al de wavesurfer. De todos modos, hay algunas tramas con valores "outliers".
  
  * Optimice los parámetros de su sistema de detección de pitch e inserte una tabla con las tasas de error
    y el *score* TOTAL proporcionados por `pitch_evaluate` en la evaluación de la base de datos 
	`pitch_db/train`..

  | **Unvoiced frames as voiced** | **Voiced frames as unvoiced** | **Gross of voiced errors (+20%)** | **MSE of fine errors** |
  |---------------------------|---------------------------|-------------------------------|--------------------|
  | 6,25%                     | 7,29%                     | 2,57%                         | 2,69%              |
  | **TOTAL**                 | 89,95%                    |                               |                    |

  Los parámetros que hemos optimizado son los que determinan si un frame es sordo o sonoro. El mejor resultado lo hemos obtenido con `pot < -40`, `r1norm <= 0.92` y `rmaxnorm <= 0.53`. Aparte de estos valores hemos modificado también la ventana y hemos usado la ventana rectangular.

   * Inserte una gráfica en la que se vea con claridad el resultado de su detector de pitch junto al del
     detector de Wavesurfer. Aunque puede usarse Wavesurfer para obtener la representación, se valorará
	 el uso de alternativas de mayor calidad (particularmente Python).

   <img src="pitch_plot.png" width="640" align="center">

   

Ejercicios de ampliación
------------------------

- Usando la librería `docopt_cpp`, modifique el fichero `get_pitch.cpp` para incorporar los parámetros del
  detector a los argumentos de la línea de comandos.
  
  Esta técnica le resultará especialmente útil para optimizar los parámetros del detector. Recuerde que
  una parte importante de la evaluación recaerá en el resultado obtenido en la detección de pitch en la
  base de datos.

  * Inserte un *pantallazo* en el que se vea el mensaje de ayuda del programa y un ejemplo de utilización
    con los argumentos añadidos.

- Implemente las técnicas que considere oportunas para optimizar las prestaciones del sistema de detección
  de pitch.

  Entre las posibles mejoras, puede escoger una o más de las siguientes:

  * Técnicas de preprocesado: filtrado paso bajo, *center clipping*, etc.
  * Técnicas de postprocesado: filtro de mediana, *dynamic time warping*, etc.
  * Métodos alternativos a la autocorrelación: procesado cepstral, *average magnitude difference function*
    (AMDF), etc.
  * Optimización **demostrable** de los parámetros que gobiernan el detector, en concreto, de los que
    gobiernan la decisión sonoro/sordo.
  * Cualquier otra técnica que se le pueda ocurrir o encuentre en la literatura.

  Encontrará más información acerca de estas técnicas en las [Transparencias del Curso](https://atenea.upc.edu/pluginfile.php/2908770/mod_resource/content/3/2b_PS%20Techniques.pdf)
  y en [Spoken Language Processing](https://discovery.upc.edu/iii/encore/record/C__Rb1233593?lang=cat).
  También encontrará más información en los anexos del enunciado de esta práctica.

  Incluya, a continuación, una explicación de las técnicas incorporadas al detector. Se valorará la
  inclusión de gráficas, tablas, código o cualquier otra cosa que ayude a comprender el trabajo realizado.

  También se valorará la realización de un estudio de los parámetros involucrados. Por ejemplo, si se opta
  por implementar el filtro de mediana, se valorará el análisis de los resultados obtenidos en función de
  la longitud del filtro.
   

Evaluación *ciega* del detector
-------------------------------

Antes de realizar el *pull request* debe asegurarse de que su repositorio contiene los ficheros necesarios
para compilar los programas correctamente ejecutando `make release`.

Con los ejecutables construidos de esta manera, los profesores de la asignatura procederán a evaluar el
detector con la parte de test de la base de datos (desconocida para los alumnos). Una parte importante de
la nota de la práctica recaerá en el resultado de esta evaluación.
