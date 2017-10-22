package com.bounswe2017.group10.atlas.home;


import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.design.widget.TabLayout;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentActivity;
import android.support.v4.view.ViewPager;

import com.bounswe2017.group10.atlas.R;
import com.bounswe2017.group10.atlas.adapter.TabPagerAdapter;
import com.bounswe2017.group10.atlas.util.Constants;


public class HomeActivity extends FragmentActivity {

    private static final String TAG = "HomeActivity";


    private String authStr;
    private TabPagerAdapter mAdapter;
    private ViewPager mPager;
    private TabLayout mTabs;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        authStr = getIntent().getStringExtra(Constants.AUTH_STR);

        setContentView(R.layout.activity_home);

        // set swiping
        mAdapter = initAdapter();
        mTabs = findViewById(R.id.tabs);
        mPager = findViewById(R.id.pager);
        mPager.setAdapter(mAdapter);
        mTabs.setupWithViewPager(mPager);

        mPager.addOnPageChangeListener(new ViewPager.SimpleOnPageChangeListener() {
            @Override
            public void onPageSelected(int position) {
                mPager.setCurrentItem(position);
                super.onPageSelected(position);
            }
        });

    }

    private TabPagerAdapter initAdapter() {
        Bundle bundle = new Bundle();
        bundle.putString(Constants.AUTH_STR, authStr);

        Fragment feedFragment = new FeedFragment();
        feedFragment.setArguments(bundle);
        Fragment createItemFragment = new CreateItemFragment();
        createItemFragment.setArguments(bundle);

        TabPagerAdapter adapter = new TabPagerAdapter(getSupportFragmentManager());
        adapter.addFragment(feedFragment, getResources().getString(R.string.feed));
        adapter.addFragment(createItemFragment, getResources().getString(R.string.create));
        return adapter;
    }
}


