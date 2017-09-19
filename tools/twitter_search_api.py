import os
import argparse
import json
import sys

if sys.version_info.major == 2:
    import ConfigParser as configparser
else:
    import configparser
import logging

try:
    from cStringIO import StringIO
except ImportError:
    try:
        from StringIO import StringIO
    except ModuleNotFoundError:
        from io import StringIO


from twittersearchapi.result_stream import ResultStream
from twittersearchapi.utils import gen_endpoint
from twittersearchapi.utils import *


def parse_cmd_args():
    twitter_parser = argparse.ArgumentParser()

    twitter_parser.add_argument("--config-file", dest="config_filename",
                                default=None,
                                help=("configuration file with all parameters. Far",
                                      "easier to use than the command-line args version.",
                                      "If a valid file is found, all args will be populated",
                                      "from there. Remaining command-line args",
                                      "will overrule args found in the config",
                                      "file."))

    twitter_parser.add_argument("--account-name",
                                dest="account_name",
                                default=None,
                                help="Gnip API account name")

    twitter_parser.add_argument("--user-name",
                                dest="username",
                                default=None,
                                help="User name")

    twitter_parser.add_argument("--password",
                                dest="password",
                                default=None,
                                help="Password")

    twitter_parser.add_argument("--count-bucket",
                                dest="count_bucket",
                                default=None,
                                help=("Bucket size for counts query. Options",
                                      "are day, hour, minute (default is 'day')."))

    twitter_parser.add_argument("--start-datetime",
                                dest="from_date",
                                default=None,
                                help="Start of datetime window, format 'YYYY-mm-DDTHH:MM' (default: 30 days ago)")

    twitter_parser.add_argument("--end-datetime", dest="to_date",
                                default=None,
                                help="End of datetime window, format 'YYYY-mm-DDTHH:MM' (default: most recent activities)")

    twitter_parser.add_argument("--filter-rule", dest="pt_rule",
                                default="beyonce has:geo",
                                help="PowerTrack filter rule (See: http://support.gnip.com/customer/portal/articles/901152-powertrack-operators)")

    twitter_parser.add_argument("--stream-endpoint",
                                dest="endoint_label",
                                default=None,
                                help="Url of search endpoint. (See your Gnip console.)")

    twitter_parser.add_argument("--results-max", dest="results_max",
                                default=500,
                                help="Maximum results to return per api call (default 500; max 500)")

    twitter_parser.add_argument("--max_tweets", dest="max_tweets",
                                default=500,
                                type=int,
                                help="Maximum results to return for all pages; see -a option")

    
    twitter_parser.add_argument("--results-per-file", dest="results_per_file",
                                default=0,
                                type=int,
                                help="Maximum tweets to save per file.")


    twitter_parser.add_argument("--filename-prefix",
                                dest="filename_prefix",
                                default=None,
                                help="prefix for the filename where tweet json data will be stored."
                               )

    twitter_parser.add_argument("--output-file-path",
                                dest="output_file_path",
                                default=None,
                                help=("Create files in ./OUTPUT-FILE-PATH. This path must exist &",
                                      "will not be created. This option is available only with -a",
                                      "option. Default is no output files."))

    twitter_parser.add_argument("--no-print-stream",
                                dest="print_stream",
                                action="store_false",
                                help="disable print streaming")

    twitter_parser.add_argument("--print-stream",
                                dest="print_stream",
                                action="store_true",
                                default=True,
                                help="Print tweet stream to stdout")

    return twitter_parser


def merge_args(cmd_args, config_args):
    pass


def main():
    args_dict = vars(parse_cmd_args().parse_args())
    print(json.dumps(args_dict, indent=4))

    if "config_filename" in args_dict:
        configfile_dict = read_configfile(args_dict["config_filename"])

    print(json.dumps(configfile_dict, indent=4))
    dict_filter = lambda x: {k: v for k, v in x.items() if v is not None}
    config_dict = merge_dicts(dict_filter(configfile_dict),
                              dict_filter(args_dict))
    stream_params = gen_params_from_config(config_dict)

    print(json.dumps(config_dict, indent=4))

    rs = ResultStream(**stream_params, tweetify=False)

    if "filename_prefix" in config_dict:
        stream = write_result_stream(rs,
                                     filename_prefix=config_dict["filename_prefix"],
                                     results_per_file=config_dict["results_per_file"],
                                     passthrough_stream=True,
                                    )
    else:
        stream = rs.stream()

    for tweet in stream:
        if config_dict["print_stream"] is True:
            print(tweet)
        else:
            _ = tweet


if __name__ == '__main__':
    main()
