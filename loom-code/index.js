// OpenCode v2 entry point; the shared loader is generated into opencode/.
import { setup } from "./opencode/loader.js";

export default { id: "loom-code", setup: (ctx) => setup(ctx) };
