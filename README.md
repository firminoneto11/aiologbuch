# nlogging

### A native asyncio logging library for python.

Just a quick note, this is still a work in progress.

## Installation

```bash
# pip
$ pip install nlogging

# poetry
$ poetry add nlogging

# If you want to use a faster json parsing
$ pip install nlogging[orjson]

# If you want to use a native asyncio file handling
$ pip install nlogging[aiofile]

# If you want to use both
$ pip install nlogging[all]
```

## Usage

It's as simple as this:

```python
from nlogging import get_logger

logger = get_logger(name="my-cool-logger")

await logger.info("Hello, world!")
```

This should be enough to get you started with logging to the `stderr`, but if you wanna
know more, keep reading.

## Immutability

When you call `get_logger`, it returns an `Nlogger` instance. The library was designed
in such a way that you can't mutate the logger instance. This is to prevent any
unexpected behavior.

Once you call the `get_logger` function and setup it's properties, you can't change
them. If you want a logger with different properties, you have to call `get_logger`
again, but specifying a different name, to get a new logger instance.

It's also worth mentioning that, if you call `get_logger` with the same name, it will
return the same logger instance. This is to prevent having multiple loggers with the
same name, ensuring integrity. Only the first logger instance will have the attributes
you specified in the first call. The other calls won't have any effect, besides returning
the same logger instance.

Now, let's talk about the properties you can set.

## Level

The level property is used to specify the minimum level of logs that will be logged.

```python
from nlogging import get_logger

logger = get_logger(name="my-cool-logger", level="INFO")

await logger.info("Hello, world!")
await logger.debug("This won't be logged")
```

As you can see, theres a parameter called `level` that indicates the logger's level.
The default value is `INFO`, but you can set it to any of the following values:

- `DEBUG`

- `INFO`

- `WARNING`

- `ERROR`

- `CRITICAL`

You can either use the literal string, or the corresponding constant from the `logging`
module.

If you prefer, you can also import an enum called `LogLevel` from the `nlogging`
module, and use it instead.

```python
from nlogging import get_logger, LogLevel

logger = get_logger(name="my-cool-logger", level=LogLevel.INFO)

await logger.info("Hello, world!")
await logger.debug("This won't be logged")
```

Once again, calling `get_logger` with the same name will return the same logger
instance, so if you want to log to a different level, you have to call `get_logger`
again, but specifying a different name.

## Filename

The filename property is used to specify the file where the logs will be written to.

```python
from nlogging import get_logger

logger = get_logger(name="my-cool-logger", filename="my-cool-logger.log")

await logger.info("Hello, world!")
```

As you can see, theres a parameter called `filename` that indicates the logger's
filename. The default value is an empty string, but you can set it to any string, as
long the value is a valid path filename. If it doesn't exists, it will be created.

Once again, calling `get_logger` with the same name will return the same logger
instance, so if you want to log to a different file, you have to call `get_logger`
again, but specifying a different name.

It's worth mentioning that the file logging is async native if you have the `aiofile`
package installed. If you don't have it installed, it will fallback to the `threading`
approach, provided by [`anyio`](https://anyio.readthedocs.io/en/stable/streams.html#file-streams).

## Exclusive

The exclusive property is used to determine if the logger should log exclusively to the
level that it was specified. For example, if you set the level to `ERROR`, and the
exclusive property to `True`, the logger will only log `ERROR` messages.

But, this will only be applied if you set a `filename`. Meaning that, if you don't set a
`filename`, the logger will log to the `stderr` as if the exclusive property was set to
`False`.

So, if you want to log a level exclusively to a file, you can do something like this:

```python
from nlogging import get_logger

error_logger = get_logger(
    name="my-cool-logger",
    level='ERROR',
    filename="my-cool-error-logger.log",
    exclusive=True,
)

await error_logger.info("This won't be logged")
await error_logger.error("This will be logged only to the file")
```

It's quite useful when you want to log only errors to a file.

But keep in mind that if you wanna log the other levels, you have to create another
logger instance, with a different name.

## License

This project is licensed under the terms of the MIT license.
