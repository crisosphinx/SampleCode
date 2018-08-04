# hf_renameDuplicates v0.2 by henry foster (henry@toadstorm.com)
import sys
import maya.cmds as cm
import Modules.decoder as decoder
reload(decoder)


class Rename:
    def __init__(self, padding=int()):
        self.padding = padding
        # remove all badly named characters from scene

    def duplicates(self):
        # Get all xforms. If an xform name contains a '|', it is appearing
        # more than once and we will have to rename it.
        _bad_xforms = [f for f in cm.ls() if '|' in f]
        _bad_xforms_unlock = [
            f for f in _bad_xforms if cm.lockNode(f, q=1, lock=1)[0] is False
        ]

        count = 0
        # We need to somehow sort this list by the number of '|' appearing
        # in each name. This way we can edit names from the bottom of
        # the hierarchy up, and not worry about losing child objects
        # from the list.
        count_dict = {}
        for f in _bad_xforms_unlock:
            count_dict[f] = f.count('|')
        # Now sort the dictionary by value, in reverse, and start renaming.

        for key, value in sorted(
                count_dict.iteritems(),
                reverse=True,
                key=lambda (key, value): (value, key)
        ):
            # Okay, now we can start actually renaming objects in order.
            n = 1
            # print '\ndebug: renaming object {}\n'.format(key)
            _new_key = (
                key.split('|')[-1] +
                '_' +
                str(n).zfill(self.padding)
            )
            _new_obj = cm.rename(
                key,
                _new_key
            )

            while _new_obj.count('|') > 0:
                # INFINITE LOOP PROBLEM: If the transform and the shape are
                # named the same, this will go on forever. We need to write
                # some kind of exception to prevent this from happening.
                n += 1
                _basename = _new_obj.split('|')[-1]
                _new_name = (
                    '_'.join(_basename.split('_')[0:-1]) +
                    '_' +
                    str(n).zfill(self.padding)
                )
                _new_obj = cm.rename(_new_obj, _new_name)

            # print('renamed {} to {}'.format(key, _new_obj))
            count += 1

        if count < 1:
            return 'No duplicate names found.'

        else:
            return(
                'Found and renamed ' +
                str(count) +
                ' objects with duplicate names.'
                # ' Check script editor for details.'
            )


def main(padding=3):
    _info1 = (Rename(padding).duplicates())
    _info2 = decoder.main(_info1)
    sys.stdout.write(_info2)
    return _info2
