# this shows a pop up message if SWAP file has less than 25% left For those
# wondering, whether system is usable at that moment: well, with ZSWAP enabled on 5.3
# and later kernel (at least with an SSD disk) there's no lags until the moment SWAP
# is 100% ful.
$user_alerted=0;
while (1) {
    $free_output=`free`;
    foreach (split(/\n/, $free_output)) {
        if (/^Swap/) {
            $used=$F[2];
            $total=$F[1];
            $threshold=$total*0.75;
            if ($threshold <= $used) {
                if (not $user_alerted) {
                    `notify-send "Warning" "Your memory is low!"`;
                    $user_alerted = 1;
                }
            } else {
                $user_alerted = 0;
            }
        }
    }
    sleep(5);
}
