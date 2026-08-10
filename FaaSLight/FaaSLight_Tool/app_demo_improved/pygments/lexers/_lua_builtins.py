"""
    pygments.lexers._lua_builtins
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This file contains the names and modules of lua functions
    It is able to re-generate itself, but for adding new functions you
    probably have to add some callbacks (see function module_callbacks).

    Do not edit the MODULES dict by hand.

    Run with `python -I` to regenerate.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

MODULES = {'basic': ('_G', '_VERSION', 'assert', 'collectgarbage', 'dofile', 'error', 'getmetatable', 'ipairs', 'load', 'loadfile', 'next', 'pairs', 'pcall', 'print', 'rawequal', 'rawget', 'rawlen', 'rawset', 'select', 'setmetatable', 'tonumber', 'tostring', 'type', 'warn', 'xpcall'), 'bit32': ('bit32.arshift', 'bit32.band', 'bit32.bnot', 'bit32.bor', 'bit32.btest', 'bit32.bxor', 'bit32.extract', 'bit32.lrotate', 'bit32.lshift', 'bit32.replace', 'bit32.rrotate', 'bit32.rshift'), 'coroutine': ('coroutine.close', 'coroutine.create', 'coroutine.isyieldable', 'coroutine.resume', 'coroutine.running', 'coroutine.status', 'coroutine.wrap', 'coroutine.yield'), 'debug': ('debug.debug', 'debug.gethook', 'debug.getinfo', 'debug.getlocal', 'debug.getmetatable', 'debug.getregistry', 'debug.getupvalue', 'debug.getuservalue', 'debug.sethook', 'debug.setlocal', 'debug.setmetatable', 'debug.setupvalue', 'debug.setuservalue', 'debug.traceback', 'debug.upvalueid', 'debug.upvaluejoin'), 'io': ('io.close', 'io.flush', 'io.input', 'io.lines', 'io.open', 'io.output', 'io.popen', 'io.read', 'io.stderr', 'io.stdin', 'io.stdout', 'io.tmpfile', 'io.type', 'io.write'), 'math': ('math.abs', 'math.acos', 'math.asin', 'math.atan', 'math.atan2', 'math.ceil', 'math.cos', 'math.cosh', 'math.deg', 'math.exp', 'math.floor', 'math.fmod', 'math.frexp', 'math.huge', 'math.ldexp', 'math.log', 'math.max', 'math.maxinteger', 'math.min', 'math.mininteger', 'math.modf', 'math.pi', 'math.pow', 'math.rad', 'math.random', 'math.randomseed', 'math.sin', 'math.sinh', 'math.sqrt', 'math.tan', 'math.tanh', 'math.tointeger', 'math.type', 'math.ult'), 'modules': ('package.config', 'package.cpath', 'package.loaded', 'package.loadlib', 'package.path', 'package.preload', 'package.searchers', 'package.searchpath', 'require'), 'os': ('os.clock', 'os.date', 'os.difftime', 'os.execute', 'os.exit', 'os.getenv', 'os.remove', 'os.rename', 'os.setlocale', 'os.time', 'os.tmpname'), 'string': ('string.byte', 'string.char', 'string.dump', 'string.find', 'string.format', 'string.gmatch', 'string.gsub', 'string.len', 'string.lower', 'string.match', 'string.pack', 'string.packsize', 'string.rep', 'string.reverse', 'string.sub', 'string.unpack', 'string.upper'), 'table': ('table.concat', 'table.insert', 'table.move', 'table.pack', 'table.remove', 'table.sort', 'table.unpack'), 'utf8': ('utf8.char', 'utf8.charpattern', 'utf8.codepoint', 'utf8.codes', 'utf8.len', 'utf8.offset')}
if __name__ == '__main__':
    import re
    from urllib.request import urlopen
    import pprint
    
    def module_callbacks():
        import custom_funtemplate
        return custom_funtemplate.rewrite_template('pygments.lexers._lua_builtins.module_callbacks', 'module_callbacks()', {}, 1)
    
    def get_newest_version():
        import custom_funtemplate
        return custom_funtemplate.rewrite_template('pygments.lexers._lua_builtins.get_newest_version', 'get_newest_version()', {'urlopen': urlopen, 're': re}, 1)
    
    def get_lua_functions(version):
        import custom_funtemplate
        return custom_funtemplate.rewrite_template('pygments.lexers._lua_builtins.get_lua_functions', 'get_lua_functions(version)', {'urlopen': urlopen, 're': re, 'version': version}, 1)
    
    def get_function_module(name):
        import custom_funtemplate
        return custom_funtemplate.rewrite_template('pygments.lexers._lua_builtins.get_function_module', 'get_function_module(name)', {'module_callbacks': module_callbacks, 'name': name}, 1)
    
    def regenerate(filename, modules):
        import custom_funtemplate
        custom_funtemplate.rewrite_template('pygments.lexers._lua_builtins.regenerate', 'regenerate(filename, modules)', {'pprint': pprint, 'filename': filename, 'modules': modules}, 0)
    
    def run():
        import custom_funtemplate
        custom_funtemplate.rewrite_template('pygments.lexers._lua_builtins.run', 'run()', {'get_newest_version': get_newest_version, 'get_lua_functions': get_lua_functions, 'get_function_module': get_function_module, 'regenerate': regenerate, '__file__': __file__}, 0)
    run()

