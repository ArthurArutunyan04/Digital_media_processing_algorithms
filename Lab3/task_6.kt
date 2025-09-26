import java.awt.image.BufferedImage
import java.io.File
import javax.imageio.ImageIO
import kotlin.math.exp
import kotlin.math.PI

fun gaussianMatrix(size: Int, sigma: Double): Array<DoubleArray> {
    val matrix = Array(size) { DoubleArray(size) }
    val center = size / 2
    var sum = 0.0

    for (x in 0 until size) {
        for (y in 0 until size) {
            val dx = x - center
            val dy = y - center
            val value = (1.0 / (2 * PI * sigma * sigma)) * exp(-(dx * dx + dy * dy) / (2 * sigma * sigma))
            matrix[x][y] = value
            sum += value
        }
    }

    for (x in 0 until size) {
        for (y in 0 until size) {
            matrix[x][y] /= sum
        }
    }

    return matrix
}

fun gaussianBlur(image: BufferedImage, kernel: Array<DoubleArray>): BufferedImage {
    val width = image.width
    val height = image.height
    val result = BufferedImage(width, height, BufferedImage.TYPE_INT_RGB)
    val kSize = kernel.size
    val pad = kSize / 2

    for (x in 0 until width) {
        for (y in 0 until height) {
            var rSum = 0.0
            var gSum = 0.0
            var bSum = 0.0

            for (i in 0 until kSize) {
                for (j in 0 until kSize) {
                    val xi = (x + i - pad).coerceIn(0, width - 1)
                    val yj = (y + j - pad).coerceIn(0, height - 1)
                    val rgb = image.getRGB(xi, yj)
                    val weight = kernel[i][j]

                    rSum += ((rgb shr 16) and 0xFF) * weight
                    gSum += ((rgb shr 8) and 0xFF) * weight
                    bSum += (rgb and 0xFF) * weight
                }
            }

            val r = rSum.coerceIn(0.0, 255.0).toInt()
            val g = gSum.coerceIn(0.0, 255.0).toInt()
            val b = bSum.coerceIn(0.0, 255.0).toInt()
            val rgb = (r shl 16) or (g shl 8) or b
            result.setRGB(x, y, rgb)
        }
    }
    return result
}

fun main() {
    val inputFile = File("Image.png")
    val outputFile = File("Image_gaussian_kotlin.png")

    val image = ImageIO.read(inputFile)

    val kernelSize = 5
    val sigma = 1.5

    val kernel = gaussianMatrix(kernelSize, sigma)
    val blurredImage = gaussianBlur(image, kernel)

    ImageIO.write(blurredImage, "png", outputFile)
    println("Размытие Гаусса завершено, сохранено в ${outputFile.name}")
}


/*

kotlinc task_6.kt -include-runtime -d task_6.jar && java -jar task_6.jar

*/