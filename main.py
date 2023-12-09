from helper.display import init
from helper.actions import runFunctionFromJson, addMod
from helper.args_handler import parser


if __name__ == "__main__":
    args = parser.parse_args()
    if args.modPath:
        addMod(args.modPath)

    a = init()
    runFunctionFromJson(a)
