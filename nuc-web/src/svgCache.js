// SVGCache.js
/**
 * SVGCache class to cache SVG files and their contents.
 * It uses the require.context function to traverse the assets folder and
 * preload SVG files.
 */
class SVGCache {
    // Store the array of SVG file names
    static svgFileNames = [];
    // Store the object of SVG contents
    static svgContents = {};

    /**
     * Preload SVG files and their contents.
     * It only preloads the files once.
     */
    static preloadSVGs() {
        // Check if the SVG file names array is empty
        if (this.svgFileNames.length === 0) {
            // Get the require context for the assets folder
            const req = require.context('./assets', true, /\.svg$/);
            // Get the file names and replace the './' prefix
            this.svgFileNames = req.keys().map((fileName) => fileName.replace('./', ''));
            // Load the SVG contents for each file
            req.keys().forEach((fileName) => {
                let key = fileName.replace('./', '');
                this.svgContents[key] = req(fileName);
            });
        }
    }

    /**
     * Get the array of SVG file names.
     * @returns {Array} The array of SVG file names.
     */
    static getSVGFileNames() {
        return this.svgFileNames;
    }

    /**
     * Get the SVG content for a given file name.
     * @param {string} fileName - The name of the SVG file.
     * @returns {string} The SVG content.
     */
    static getSVGContent(fileName) {
        return this.svgContents[fileName];
    }
}

export default SVGCache;
