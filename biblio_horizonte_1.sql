-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 23-05-2026 a las 08:01:48
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `biblio_horizonte_1`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `administradores`
--

CREATE TABLE `administradores` (
  `id_admin` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `correo` varchar(100) NOT NULL,
  `contraseña` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `administradores`
--

INSERT INTO `administradores` (`id_admin`, `nombre`, `correo`, `contraseña`) VALUES
(1, 'Leo', 'leo@biblio.com', 'admin123'),
(2, 'Lizeth', 'lizz@biblio.com', 'admin456');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `devolucion`
--

CREATE TABLE `devolucion` (
  `id_devolucion` int(11) NOT NULL,
  `titulo_libro` varchar(255) NOT NULL,
  `nombre_prestamista` varchar(255) NOT NULL,
  `fecha` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `devolucion`
--

INSERT INTO `devolucion` (`id_devolucion`, `titulo_libro`, `nombre_prestamista`, `fecha`) VALUES
(1, '1984', 'Juanito', '2026-05-19 20:38:20'),
(2, 'paula', 'juan martinez', '2026-05-19 20:42:08'),
(3, 'cien años de soledad', 'Juanito', '2026-05-19 21:20:29'),
(4, '1984', 'mar aguilar', '2026-05-19 21:21:31'),
(5, 'paula', 'yoyo', '2026-05-19 21:45:52'),
(6, 'la sombra del viento', 'leonardo', '2026-05-20 07:45:48'),
(7, 'la sombra del viento', 'luis lopez', '2026-05-20 08:07:55'),
(8, 'la fiesta del chivo', 'pedro hernandez', '2026-05-20 08:09:58'),
(9, 'la casa de los espiritus', 'mar aguilar', '2026-05-20 19:19:35'),
(10, 'la sombra del viento', 'leonardo', '2026-05-20 20:26:59');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `historial`
--

CREATE TABLE `historial` (
  `id_historial` int(11) NOT NULL,
  `titulo_libro` varchar(150) NOT NULL,
  `nombre_prestamista` varchar(100) NOT NULL,
  `fecha` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `libros`
--

CREATE TABLE `libros` (
  `id_libro` int(11) NOT NULL,
  `titulo` varchar(150) NOT NULL,
  `autor` varchar(100) NOT NULL,
  `categoria` varchar(100) DEFAULT NULL,
  `isbn` varchar(50) DEFAULT NULL,
  `cantidad` int(11) NOT NULL,
  `disponibles` int(11) NOT NULL,
  `descripcion` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `libros`
--

INSERT INTO `libros` (`id_libro`, `titulo`, `autor`, `categoria`, `isbn`, `cantidad`, `disponibles`, `descripcion`) VALUES
(1, 'Cien Años de Soledad', 'Gabriel Garcia Marquez', 'Novela', '9780307474728', 5, 3, 'Historia de la familia Buendia en Macondo'),
(2, '1984', 'George Orwell', 'Distopia', '9780451524935', 3, 0, 'Sociedad controlada por el Gran Hermano'),
(3, 'El Principito', 'Antoine de Saint-Exupery', 'Infantil', '9780156012195', 4, 2, 'Fabula sobre la vida y la amistad'),
(4, 'Don Quijote de la Mancha', 'Miguel de Cervantes', 'Clasico', '9788491050295', 2, 2, 'Historia del caballero andante'),
(5, 'La Casa de los Espiritus', 'Isabel Allende', 'Novela', '9780553383805', 6, 6, 'Saga familiar ambientada en Chile con elementos de realismo magico'),
(6, 'Paula', 'Isabel Allende', 'Biografico', '9780060542183', 4, 3, 'Memoria escrita por Isabel Allende dedicada a su hija'),
(7, 'Como Agua para Chocolate', 'Laura Esquivel', 'Realismo Magico', '9780385420174', 5, 5, 'Historia de amor y tradicion mexicana mezclada con cocina'),
(8, 'La Sombra del Viento', 'Carlos Ruiz Zafon', 'Misterio', '9788408172178', 5, 5, 'Novela ambientada en Barcelona sobre libros y secretos'),
(9, 'El Amor en los Tiempos del Colera', 'Gabriel Garcia Marquez', 'Novela', '9780307389732', 3, 3, 'Historia de amor que perdura durante decadas'),
(10, 'La Fiesta del Chivo', 'Mario Vargas Llosa', 'Novela Historica', '9780374536996', 4, 4, 'Relato sobre la dictadura de Trujillo en Republica Dominicana'),
(11, 'La Casa de los Conejos', 'Laura Alcoba', 'Novela Historica', '9789876290199', 3, 3, 'Historia ambientada en la dictadura argentina'),
(12, 'Arrancame la Vida', 'Angeles Mastretta', 'Novela', '9789684110787', 4, 4, 'Historia de una mujer en el Mexico posrevolucionario'),
(13, 'Del Amor y Otros Demonios', 'Gabriel Garcia Marquez', 'Novela', '9780307473134', 3, 3, 'Historia inspirada en una leyenda colonial'),
(15, 'El Cuaderno de Maya', 'Isabel Allende', 'Novela', '9788401340468', 4, 3, 'Cuenta las peripecias de una joven perdida en el mundo del alcohol, las drogas y cómo poco a poco se abre paso hacia una nueva vida.'),
(16, 'Pedro Paramo', 'Juan Rulfo', 'Realismo Magico', '9789685208536', 5, 5, 'Un viaje a Comala, un pueblo de murmullos y fantasmas'),
(17, 'Ficciones', 'Jorge Luis Borges', 'Literatura', '9788420633138', 4, 4, 'Coleccion de cuentos que desafian la logica y el tiempo'),
(18, 'Rayuela', 'Julio Cortazar', 'Novela', '9788420471013', 3, 3, 'Novela contranovela que se puede leer en multiples ordenes'),
(19, 'Frankenstein', 'Mary Shelley', 'Terror', '9780143131847', 4, 4, 'Clasico de ciencia ficcion sobre el doctor y su criatura'),
(20, 'Dune', 'Frank Herbert', 'Ciencia Ficcion', '9780441172719', 6, 6, 'Epopeya planetaria sobre politica, religion y ecologia'),
(21, 'Dracula', 'Bram Stoker', 'Terror', '9780486411095', 5, 5, 'La legendaria historia del conde vampiro de Transilvania'),
(22, 'El Tunel', 'Ernesto Sabato', 'Novela Psicologica', '9788432248221', 3, 3, 'La obsesion y confesion del pintor Juan Pablo Castel'),
(23, 'Los de Abajo', 'Mariano Azuela', 'Novela Historica', '9789681602741', 4, 4, 'Cronica fundamental sobre la Revolucion Mexicana'),
(24, 'Fahrenheit 451', 'Ray Bradbury', 'Distopia', '9781451673319', 5, 5, 'Una sociedad del futuro donde los libros estan prohibidos'),
(25, 'El Retrato de Dorian Gray', 'Oscar Wilde', 'Clasico', '9780141439570', 4, 4, 'La busqueda de la eterna juventud y la decadencia moral'),
(26, 'La Tregua', 'Mario Benedetti', 'Novela', '9788420655475', 5, 5, 'El diario de Martin Santome y su inesperado romance'),
(27, 'Un Mundo Feliz', 'Aldous Huxley', 'Distopia', '9780060850524', 4, 4, 'Una sociedad perfecta controlada por la tecnologia y el consumo'),
(28, 'Metamorfosis', 'Franz Kafka', 'Ficcion Absurda', '9788420651361', 3, 3, 'La historia de Gregorio Samsa al amanecer transformado en insecto'),
(29, 'El Alquimista', 'Paulo Coelho', 'Narrativa', '9780062315007', 6, 6, 'El viaje de Santiago en busca de su leyenda personal'),
(30, 'El Hobbit', 'J.R.R. Tolkien', 'Fantasia', '9780345339683', 5, 5, 'Las aventuras de Bilbo Bolson y el viaje hacia la Montana Solitaria');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `prestamo`
--

CREATE TABLE `prestamo` (
  `id_prestamo` int(11) NOT NULL,
  `titulo_libro` varchar(150) NOT NULL,
  `nombre_prestamista` varchar(100) NOT NULL,
  `fecha` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `prestamo`
--

INSERT INTO `prestamo` (`id_prestamo`, `titulo_libro`, `nombre_prestamista`, `fecha`) VALUES
(1, '1984', 'leonardo', '0000-00-00 00:00:00'),
(3, 'cien años de soledad', 'Maria', '2026-05-19 20:39:10'),
(4, 'el principito', 'Pedro', '2026-05-19 20:40:25'),
(5, 'el principito', 'Mariana', '2026-05-19 20:41:03'),
(9, '1984', 'leon', '2026-05-19 21:22:49'),
(10, '1984', 'Juanito', '2026-05-19 21:43:14'),
(15, 'paula', 'leonardo nuñez', '2026-05-20 08:10:56'),
(18, 'el cuaderno de maya', 'Lizeth', '2026-05-20 20:27:14');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `administradores`
--
ALTER TABLE `administradores`
  ADD PRIMARY KEY (`id_admin`),
  ADD UNIQUE KEY `correo` (`correo`);

--
-- Indices de la tabla `devolucion`
--
ALTER TABLE `devolucion`
  ADD PRIMARY KEY (`id_devolucion`);

--
-- Indices de la tabla `historial`
--
ALTER TABLE `historial`
  ADD PRIMARY KEY (`id_historial`);

--
-- Indices de la tabla `libros`
--
ALTER TABLE `libros`
  ADD PRIMARY KEY (`id_libro`);

--
-- Indices de la tabla `prestamo`
--
ALTER TABLE `prestamo`
  ADD PRIMARY KEY (`id_prestamo`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `administradores`
--
ALTER TABLE `administradores`
  MODIFY `id_admin` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `devolucion`
--
ALTER TABLE `devolucion`
  MODIFY `id_devolucion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `historial`
--
ALTER TABLE `historial`
  MODIFY `id_historial` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `libros`
--
ALTER TABLE `libros`
  MODIFY `id_libro` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT de la tabla `prestamo`
--
ALTER TABLE `prestamo`
  MODIFY `id_prestamo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
