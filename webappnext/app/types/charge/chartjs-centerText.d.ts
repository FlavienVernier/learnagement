/**
 * Declaration file augmenting the Chart.js types to support a custom "centerText" plugin option.
 *
 * IMPORTANT:
 * - This file should only contain type definitions (no runtime code).
 * - Make sure it is placed in a folder included by your "tsconfig.json" under "include".
 * - Do NOT import this file in your runtime code. With Next.js and many bundlers,
 *   .d.ts files should not be directly imported, or you'll get a parse error.
 */

import { ChartType, PluginOptionsByType } from "chart.js";

declare module "chart.js" {
    interface PluginOptionsByType<TType extends ChartType> {
        centerText?: {
            text: string | number;
        };
    }
}