# Command Executor

A Python module for executing both local and remote shell commands with support for cached connections and parallel execution.

## Features

- Execute local shell commands seamlessly.
- Run remote commands on one or multiple hosts.
- Support for serial and parallel execution of remote commands.
- Connection caching for improved performance.
- Built-in error handling for remote command execution.

## Installation

You can install the module directly from its public repository:

```bash
pip install git+https://github.com/Ekerim/command_executor.git
```

## Usage

### Running Local Commands

You can execute local shell commands using the `run_cmd` function without specifying any hosts.

```python
from command_executor import run_cmd

stdout, stderr, exit_code = run_cmd("echo 'Hello, Local!'")
print(stdout)  # Output: Hello, Local!
```

### Running Remote Commands

To execute commands on remote hosts, provide a list of hostnames. By default, commands are executed serially.

```python
stdout, stderr, exit_code = run_cmd("echo 'Hello, Remote!'", hosts=["host1", "host2"])
print(stdout)  # Output: {'host1': 'Hello, Remote!', 'host2': 'Hello, Remote!'}
```

### Parallel Execution

Enable parallel execution by setting the `parallel` parameter to `True`.

```python
stdout, stderr, exit_code = run_cmd("echo 'Hello, Parallel!'", hosts=["host1", "host2"], parallel=True)
print(stdout)  # Output: {'host1': 'Hello, Parallel!', 'host2': 'Hello, Parallel!'}
```

### Connection Caching

Connections to remote hosts are cached automatically for reuse. This improves performance when running multiple commands on the same hosts.

### Closing Connections

Connections are closed automatically when your program shuts down.

## License

This project is licensed under the GNU Lesser General Public License v3 (LGPLv3). See the [LICENSE](./LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## Contact

For questions or support, please contact [ekerim@gmail.com](mailto:ekerim@gmail.com).
