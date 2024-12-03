from pydantic_ai import Agent, ModelRetry, UnexpectedModelBehavior

agent = Agent('openai:gpt-4o')


@agent.tool_plain
def calc_volume(size: int) -> int:  # (1)!
    if size == 42:
        return size**3
    else:
        raise ModelRetry('Please try again.')


try:
    result = agent.run_sync('Please get me the volume of a box with size 6.')
except UnexpectedModelBehavior as e:
    print('An error occurred:', e)
    #> An error occurred: Tool exceeded max retries count of 1
    print('cause:', repr(e.__cause__))
    #> cause: ModelRetry('Please try again.')
    print('messages:', agent.last_run_messages)
    """
    messages:
    [
        UserPrompt(
            content='Please get me the volume of a box with size 6.',
            timestamp=datetime.datetime(...),
            role='user',
        ),
        ModelStructuredResponse(
            calls=[
                ToolCall(
                    tool_name='calc_volume',
                    args=ArgsDict(args_dict={'size': 6}),
                    tool_id=None,
                )
            ],
            timestamp=datetime.datetime(...),
            role='model-structured-response',
        ),
        RetryPrompt(
            content='Please try again.',
            tool_name='calc_volume',
            tool_id=None,
            timestamp=datetime.datetime(...),
            role='retry-prompt',
        ),
        ModelStructuredResponse(
            calls=[
                ToolCall(
                    tool_name='calc_volume',
                    args=ArgsDict(args_dict={'size': 6}),
                    tool_id=None,
                )
            ],
            timestamp=datetime.datetime(...),
            role='model-structured-response',
        ),
    ]
    """
else:
    print(result.data)