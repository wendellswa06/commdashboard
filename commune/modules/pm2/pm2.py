import os
from typing import *
import commune as c
import json

class PM2(c.Module):
    dir = os.path.expanduser('~/.pm2')
   
    @classmethod
    def restart(cls, name:str, verbose:bool = False, prefix_match:bool = True):
        list = cls.list()
        if name in list:
            rm_list = [name]
        else:
            if prefix_match:
                rm_list = [ p for p in list if p.startswith(name)]
            else:
                raise Exception(f'pm2 process {name} not found')

        if len(rm_list) == 0:
            return []
        for n in rm_list:
            c.print(f'Restarting {n}', color='cyan')
            c.cmd(f"pm2 restart {n}", verbose=False)
            cls.rm_logs(n)  
        return {'success':True, 'message':f'Restarted {name}'}
       
    @classmethod
    def restart_prefix(cls, name:str = None, verbose:bool=False):
        list = cls.list()
            
        restarted_modules = []
        
        for module in list:
            if module.startswith(name) or name in ['all']:
                if verbose:
                    c.print(f'Restarting {module}', color='cyan')
                c.cmd(f"pm2 restart {module}", verbose=verbose)
                restarted_modules.append(module)
        
        return restarted_modules
       

    @classmethod
    def kill(cls, name:str, verbose:bool = False, prefix_match:bool = True):
        list = cls.list()
        rm_list = []
        if name in list:
            rm_list = [name]

        if prefix_match:
            rm_list = [ p for p in list if p.startswith(name)]

        if len(rm_list) == 0:
            return {'success':False, 'message':f'No pm2 processes found for {name}'}
        for n in rm_list:
            if verbose:
                c.print(f'Killing {n}', color='red')
            cls.cmd(f"pm2 delete {n}", verbose=False)
            # remove the logs from the pm2 logs directory
            cls.rm_logs(n)

        return {'success':True, 'killed':rm_list, 'message':f'Killed {name}'}
    
    @classmethod
    def status(cls, verbose=True):
        stdout = cls.run_command(f"pm2 status")
        if verbose:
            c.print(stdout,color='green')
        return stdout

    dir = os.path.expanduser('~/.pm2')
    @classmethod
    def logs_path_map(cls, name=None):
        logs_path_map = {}
        for l in c.ls(f'{cls.dir}/logs/'):
            key = '-'.join(l.split('/')[-1].split('-')[:-1]).replace('-',':')
            logs_path_map[key] = logs_path_map.get(key, []) + [l]

    
        for k in logs_path_map.keys():
            logs_path_map[k] = {l.split('-')[-1].split('.')[0]: l for l in list(logs_path_map[k])}

        if name != None:
            return logs_path_map.get(name, {})

        return logs_path_map

    @classmethod
    def rm_logs( cls, name):
        logs_map = cls.logs_path_map(name)

        for k in logs_map.keys():
            c.rm(logs_map[k])

    @classmethod
    def logs(cls, 
                module:str, 
                tail: int =100, 
                verbose: bool=True ,
                mode: str ='cmd',
                **kwargs):
        
        if mode == 'local':
            text = ''
            for m in ['out','error']:

                # I know, this is fucked 
                path = f'{cls.dir}/logs/{module.replace("/", "-")}-{m}.log'.replace(':', '-').replace('_', '-')
                try:
                    text +=  c.get_text(path, tail=tail)
                    c.print(text)
                except Exception as e:
                    c.print(e)
                    continue
            
            return text
        elif mode == 'cmd':
            return cls.run_command(f"pm2 logs {module}", verbose=verbose)
        else:
            raise NotImplementedError(f'mode {mode} not implemented')
    
    


   
    @classmethod
    def kill_many(cls, search=None, verbose:bool = True, timeout=10):
        futures = []
        for name in cls.list(search=search):
            c.print(f'[bold cyan]Killing[/bold cyan] [bold yellow]{name}[/bold yellow]', color='green', verbose=verbose)
            f = c.submit(cls.kill, kwargs=dict(name=name, verbose=verbose), return_future=True, timeout=timeout)
            futures.append(f)
        return c.wait(futures)
    
    @classmethod
    def kill_all(cls, verbose:bool = True, timeout=10):
        return cls.kill_many(search=None, verbose=verbose, timeout=timeout)
                
    @classmethod
    def list(cls, search=None,  verbose:bool = False) -> List[str]:
        output_string = c.cmd('pm2 status', verbose=False)
        module_list = []
        for line in output_string.split('\n'):
            if '  default  ' in line:
                server_name = line.split('default')[0].strip()
                server_name = server_name.split(' ')[-1].strip()
                # fixes odd issue where there is a space between the name and the front 
                module_list += [server_name]
            
        if search != None:
            search_true = lambda x: any([s in x for s in search])
            module_list = [m for m in module_list if search_true(m)]
                
        return module_list

    # commune.run_command('pm2 status').stdout.split('\n')[5].split('    │')[0].split('  │ ')[-1]commune.run_command('pm2 status').stdout.split('\n')[5].split('    │')[0].split('  │ ')[-1] 
    
    @classmethod
    def exists(cls, name:str) -> bool:
        return bool(name in cls.list())
    
    @classmethod
    def start(cls, 
                path:str , 
                  name:str,
                  cmd_kwargs:str = None, 
                  refresh: bool = True,
                  verbose:bool = True,
                  force : bool = True,
                  interpreter : str = None,
                  **kwargs):
        if cls.exists(name) and refresh:
            cls.kill(name, verbose=verbose)
            
        cmd = f'pm2 start {path} --name {name}'
        if force:
            cmd += ' -f'
            
        if interpreter != None:
            cmd += f' --interpreter {interpreter}'
            
        if cmd_kwargs != None:
            cmd += f' -- '
            if isinstance(cmd_kwargs, dict):
                for k, v in cmd_kwargs.items():
                    cmd += f'--{k} {v}'
            elif isinstance(cmd_kwargs, str):
                cmd += f'{cmd_kwargs}'
                

        c.print(f'[bold cyan]Starting (PM2)[/bold cyan] [bold yellow]{name}[/bold yellow]', color='green')
            
        return c.cmd(cmd, verbose=verbose,**kwargs)
        
    @classmethod
    def launch(cls, 
                   module:str = None,  
                   fn: str = 'serve',
                   name:Optional[str]=None, 
                   tag : str = None,
                   args : list = None,
                   kwargs: dict = None,
                   device:str=None, 
                   interpreter:str='python3', 
                   auto: bool = True,
                   verbose: bool = False , 
                   force:bool = True,
                   meta_fn: str = 'module_fn',
                   tag_seperator:str = '::',
                   cwd = None,
                   refresh:bool=True ):

        if hasattr(module, 'module_path'):
            module = module.module_path()
            
        # avoid these references fucking shit up
        args = args if args else []
        kwargs = kwargs if kwargs else {}

        # convert args and kwargs to json strings
        kwargs =  {
            'module': module,
            'fn': fn,
            'args': args,
            'kwargs': kwargs
            
        }
        kwargs_str = json.dumps(kwargs).replace('"', "'")

        name = cls.resolve_server_name(module=module, name=name, tag=tag, tag_seperator=tag_seperator) 


        if refresh:
            cls.kill(name)
        
        module = c.module()
        # build command to run pm2
        
        command = f" pm2 start {c.filepath()} --name {name} --interpreter {interpreter}"

        if not auto:
            command = command + ' ' + '--no-autorestart'
        if force:
            command += ' -f '
        command = command + ''

        command = command +  f' -- --fn {meta_fn} --kwargs "{kwargs_str}"'
        env = {}
        if device != None:
            if isinstance(device, int):
                env['CUDA_VISIBLE_DEVICES']=str(device)
            if isinstance(device, list):
                env['CUDA_VISIBLE_DEVICES']=','.join(list(map(str, device)))
                
        if refresh:
            cls.kill(name)  

        cwd = cwd or module.dirpath()
        stdout = c.cmd(command, env=env, verbose=verbose, cwd=cwd)
    
        return {'success':True, 'message':f'Launched {module}', 'command': command, 'stdout':stdout}