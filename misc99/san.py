
import os
import logging
from dater import builds_dict

logger = logging.getLogger(__name__)

def get_latest_sanity(builds_dict):

    def get_datesortable_passing_builds_list():
        for build_num, build_info in builds_dict.iteritems():
            failures = build_info['failures']
            if failures != 0:
                continue
            start_time = build_info['start_time']
            path = build_info['path']
            yield start_time, build_num, path

    sorted_passing_builds_list = sorted(get_datesortable_passing_builds_list())
    sorted_passing_builds_list.reverse()

    for _, build_num, path in sorted_passing_builds_list:
        if not os.path.exists(path):
            print '{0}: does not exist (build number {1}).'.format(path, build_num)
            #logger.warn('{0}: does not exist')
            continue
        else:
            return build_num, path

    raise Exception("No passing builds found.")


if __name__ == '__main__':
    x = get_latest_sanity(builds_dict)
    print x
